# -*- coding: utf-8 -*-
import os

from fastapi import FastAPI, Depends, Response, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Optional
from sqlalchemy.orm import Session
import redis
import json

from database import SessionLocal, init_db
from models import Provider, Lead as LeadModel
from i18n import (
    DEFAULT_LANGUAGE,
    SUPPORTED_LANGUAGES,
    fetch_translations,
    resolve_translation,
    upsert_translation_values,
)

app = FastAPI(title="Nevumo API")

try:
    redis_client = redis.Redis(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=int(os.getenv("REDIS_PORT", 6379)),
        db=int(os.getenv("REDIS_DB", 0)),
        decode_responses=True,
    )
    redis_client.ping()
except Exception:
    redis_client = None

init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ProviderSchema(BaseModel):
    id: int
    name: str
    slug: str
    job_title: str
    job_title_key: str
    category: str
    category_key: str
    rating: float
    jobs_completed: int
    is_verified: bool
    city: Optional[str] = None
    profile_image_url: Optional[str] = None

    class Config:
        from_attributes = True


class ProviderCategoryUpdateSchema(BaseModel):
    category_key: str
    translations: Dict[str, str]

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/translations/{lang}")
async def get_translations(lang: str, db: Session = Depends(get_db)):
    if redis_client:
        cached_data = redis_client.get(f"translations:{lang}")
        if cached_data:
            return Response(
                content=cached_data, 
                media_type="application/json; charset=utf-8"
            )

    translations_dict = fetch_translations(db, lang)
    
    if redis_client and translations_dict:
        redis_client.setex(f"translations:{lang}", 3600, json.dumps(translations_dict, ensure_ascii=False))
        
    return Response(
        content=json.dumps(translations_dict, ensure_ascii=False), 
        media_type="application/json; charset=utf-8"
    )

@app.get("/provider-info/{provider_id}", response_model=ProviderSchema)
async def get_provider_info(
    provider_id: int,
    lang: str = Query(DEFAULT_LANGUAGE, min_length=2, max_length=5),
    db: Session = Depends(get_db),
):
    provider = db.query(Provider).filter(Provider.id == provider_id).first()
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")

    return ProviderSchema(
        id=provider.id,
        name=provider.name,
        slug=provider.slug,
        job_title=resolve_translation(db, provider.job_title, lang),
        job_title_key=provider.job_title,
        category=resolve_translation(db, provider.category, lang),
        category_key=provider.category,
        rating=provider.rating,
        jobs_completed=provider.jobs_completed,
        is_verified=provider.is_verified,
        city=provider.city,
        profile_image_url=provider.profile_image_url,
    )


@app.put("/providers/{provider_id}/category")
async def update_provider_category(
    provider_id: int,
    payload: ProviderCategoryUpdateSchema,
    db: Session = Depends(get_db),
):
    provider = db.query(Provider).filter(Provider.id == provider_id).first()
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")

    category_key = payload.category_key.strip()
    if not category_key:
        raise HTTPException(status_code=422, detail="category_key is required")

    try:
        upsert_translation_values(db, category_key, payload.translations)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    provider.category = category_key
    db.add(provider)
    db.commit()
    db.refresh(provider)

    if redis_client:
        for lang in SUPPORTED_LANGUAGES:
            redis_client.delete(f"translations:{lang}")

    return {
        "status": "success",
        "provider_id": provider.id,
        "category_key": provider.category,
        "updated_languages": len(payload.translations),
    }

@app.post("/leads/")
async def create_lead(lead: dict, db: Session = Depends(get_db)):
    new_lead = LeadModel(
        client_name=lead.get("client_name", "Client"),
        phone=lead.get("phone"),
        notes=lead.get("notes"),
        service_type=lead.get("service_type", "Lead Capture Widget")
    )
    db.add(new_lead)
    db.commit()
    db.refresh(new_lead)
    return {"status": "success", "id": new_lead.id}
