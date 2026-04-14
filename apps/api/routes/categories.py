import json
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
import redis as redis_lib

from apps.api.dependencies import get_db, get_redis
from apps.api.models import Category, CategoryTranslation
from apps.api.schemas import CategoriesResponse, CategoryOut

router = APIRouter(prefix="/api/v1", tags=["categories"])


@router.get("/categories", response_model=CategoriesResponse)
async def list_categories(
    lang: str = Query("en", min_length=2, max_length=5),
    db: Session = Depends(get_db),
    redis_client: Optional[redis_lib.Redis] = Depends(get_redis),
) -> CategoriesResponse:
    cache_key = f"categories:{lang}"

    if redis_client:
        cached = redis_client.get(cache_key)
        if cached:
            items = json.loads(cached)
            return CategoriesResponse(data=[CategoryOut(**i) for i in items])

    rows = (
        db.query(Category.id, Category.slug, CategoryTranslation.name)
        .join(CategoryTranslation, Category.id == CategoryTranslation.category_id)
        .filter(CategoryTranslation.lang == lang)
        .order_by(Category.slug)
        .all()
    )

    data = [CategoryOut(id=id, slug=slug, name=name) for id, slug, name in rows]

    if redis_client and data:
        redis_client.setex(cache_key, 3600, json.dumps([d.model_dump() for d in data], ensure_ascii=False))

    return CategoriesResponse(data=data)
