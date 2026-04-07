# -*- coding: utf-8 -*-
import json
import logging
import os

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI, Depends, Response, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from database import init_db
from dependencies import get_db, get_redis
from exceptions import NevumoException
from i18n import fetch_translations
from fastapi.staticfiles import StaticFiles
from jobs.send_magic_links import process_pending_magic_links

from routes import (
    auth_router,
    categories_router,
    cities_router,
    client_router,
    providers_router,
    leads_router,
    events_router,
    page_events_router,
    provider_router,
    reviews_router,
    user_router,
)
from routes.translations import router as translations_router
from routes.price_range import router as price_range_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

app = FastAPI(title="Nevumo API")

init_db()

# Initialize APScheduler
scheduler = BackgroundScheduler()

@app.on_event("startup")
def start_scheduler():
    def run_job():
        db = next(get_db())
        try:
            count = process_pending_magic_links(db)
            if count > 0:
                print(f"[Scheduler] Sent {count} magic links")
        except Exception as e:
            print(f"[Scheduler] Error: {e}")
        finally:
            db.close()

    scheduler.add_job(run_job, 'interval', minutes=5)
    scheduler.start()
    print("[Scheduler] Magic link job started (every 5 minutes)")

@app.on_event("shutdown")
def stop_scheduler():
    scheduler.shutdown()
    print("[Scheduler] Stopped")

origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(NevumoException)
async def nevumo_exception_handler(request: Request, exc: NevumoException) -> JSONResponse:
    content: dict = {
        "success": False,
        "error": {"code": exc.code, "message": exc.message},
    }
    if exc.extra_data:
        content["data"] = exc.extra_data
    return JSONResponse(
        status_code=exc.status_code,
        content=content,
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    errors = exc.errors()
    first = errors[0] if errors else {}
    field = ".".join(str(loc) for loc in first.get("loc", [])[1:]) if first.get("loc") else "unknown"
    message = first.get("msg", "Validation error")
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "error": {"code": "VALIDATION_ERROR", "message": f"{field}: {message}"},
        },
    )


# Include all API v1 routers
app.include_router(auth_router)
app.include_router(categories_router)
app.include_router(cities_router)
app.include_router(client_router)
app.include_router(providers_router)
app.include_router(leads_router)
app.include_router(events_router)
app.include_router(page_events_router)
app.include_router(provider_router)
app.include_router(reviews_router)
app.include_router(user_router)
app.include_router(translations_router, prefix="/api/v1")
app.include_router(price_range_router, prefix="/api/v1")

# Serve uploaded provider images
import os as _os
_os.makedirs("uploads/provider_images", exist_ok=True)
app.mount("/static/provider_images", StaticFiles(directory="uploads/provider_images"), name="provider_images")


# Keep existing translations endpoint
@app.get("/translations/{lang}")
async def get_translations(
    lang: str,
    db: Session = Depends(get_db),
    redis_client=Depends(get_redis),
) -> Response:
    if redis_client:
        cached_data = redis_client.get(f"translations:{lang}")
        if cached_data:
            return Response(
                content=cached_data,
                media_type="application/json; charset=utf-8",
            )

    translations_dict = fetch_translations(db, lang)

    if redis_client and translations_dict:
        redis_client.setex(
            f"translations:{lang}",
            3600,
            json.dumps(translations_dict, ensure_ascii=False),
        )

    return Response(
        content=json.dumps(translations_dict, ensure_ascii=False),
        media_type="application/json; charset=utf-8",
    )
