# -*- coding: utf-8 -*-
import json
import logging
import os
from dotenv import load_dotenv
load_dotenv()

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI, Depends, Response, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Any

class UnescapedJSONResponse(JSONResponse):
    media_type = "application/json; charset=utf-8"

    def render(self, content: Any) -> bytes:
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(",", ":"),
        ).encode("utf-8")

from apps.api.database import init_db
from apps.api.dependencies import get_db, get_redis
from apps.api.exceptions import NevumoException
from apps.api.i18n import fetch_translations
from fastapi.staticfiles import StaticFiles
from apps.api.jobs.retry_translations import retry_failed_translations
from apps.api.jobs.send_magic_links import process_pending_magic_links

from apps.api.routes import (
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
from apps.api.routes.price_range import router as price_range_router
from apps.api.routes.translations import router as translations_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

app = FastAPI(title="Nevumo API", default_response_class=UnescapedJSONResponse)

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

    def run_retry_translations():
        db = next(get_db())
        try:
            retry_failed_translations(db)
        except Exception as e:
            print(f"[Scheduler] Retry translations error: {e}")
        finally:
            db.close()

    scheduler.add_job(run_job, 'interval', minutes=5)
    scheduler.add_job(
        lambda: retry_failed_translations(next(get_db())),
        'cron',
        hour=3,
        minute=0,
        id='retry_translations'
    )
    scheduler.start()
    print("[Scheduler] Magic link job started (every 5 minutes)")
    print("[Scheduler] Retry translations job started (daily at 03:00)")

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
async def nevumo_exception_handler(request: Request, exc: NevumoException) -> UnescapedJSONResponse:
    content: dict = {
        "success": False,
        "error": {"code": exc.code, "message": exc.message},
    }
    if exc.extra_data:
        content["data"] = exc.extra_data
    return UnescapedJSONResponse(
        status_code=exc.status_code,
        content=content,
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> UnescapedJSONResponse:
    errors = exc.errors()
    first = errors[0] if errors else {}
    field = ".".join(str(loc) for loc in first.get("loc", [])[1:]) if first.get("loc") else "unknown"
    message = first.get("msg", "Validation error")
    return UnescapedJSONResponse(
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
