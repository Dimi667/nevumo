# -*- coding: utf-8 -*-
import json
import os

from fastapi import FastAPI, Depends, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from database import init_db
from dependencies import get_db, get_redis
from exceptions import NevumoException
from i18n import fetch_translations
from routes import (
    categories_router,
    cities_router,
    providers_router,
    leads_router,
    events_router,
)

app = FastAPI(title="Nevumo API")

init_db()

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
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {"code": exc.code, "message": exc.message},
        },
    )


# Include all API v1 routers
app.include_router(categories_router)
app.include_router(cities_router)
app.include_router(providers_router)
app.include_router(leads_router)
app.include_router(events_router)


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
