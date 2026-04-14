import json
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
import redis as redis_lib

from apps.api.constants import COUNTRY_CURRENCY_MAP, DEFAULT_CURRENCY
from apps.api.dependencies import get_db, get_redis
from apps.api.models import Location, LocationTranslation
from apps.api.schemas import CitiesResponse, CityOut

router = APIRouter(prefix="/api/v1", tags=["cities"])


@router.get("/cities", response_model=CitiesResponse)
async def list_cities(
    country: str = Query("BG", min_length=2, max_length=2),
    lang: str = Query("en", min_length=2, max_length=5),
    db: Session = Depends(get_db),
    redis_client: Optional[redis_lib.Redis] = Depends(get_redis),
) -> CitiesResponse:
    cache_key = f"cities:{country}:{lang}"

    if redis_client:
        cached = redis_client.get(cache_key)
        if cached:
            items = json.loads(cached)
            return CitiesResponse(data=[CityOut(**i) for i in items])

    rows = (
        db.query(Location)
        .outerjoin(LocationTranslation, (Location.id == LocationTranslation.location_id) & (LocationTranslation.lang == lang))
        .filter(Location.country_code == country)
        .order_by(Location.city)
        .all()
    )

    data = []
    for loc in rows:
        # Get translated city name with fallback
        translated_name = None
        if loc.translations:
            for translation in loc.translations:
                if translation.lang == lang:
                    translated_name = translation.city_name
                    break
        
        # Fallback: translation -> city_en -> city
        city_display = translated_name if translated_name else (loc.city_en if loc.city_en else loc.city)
        city_en_display = loc.city_en if loc.city_en else loc.city

        data.append(
            CityOut(
                id=loc.id,
                slug=loc.slug,
                city=city_display,
                city_en=city_en_display,
                country_code=loc.country_code,
                currency=COUNTRY_CURRENCY_MAP.get(loc.country_code, DEFAULT_CURRENCY)
            )
        )

    if redis_client and data:
        redis_client.setex(cache_key, 3600, json.dumps([d.model_dump() for d in data], ensure_ascii=False))

    return CitiesResponse(data=data)


@router.get("/cities/{slug}", response_model=CityOut)
async def get_city_by_slug(
    slug: str,
    lang: str = Query("en", min_length=2, max_length=5),
    db: Session = Depends(get_db),
    redis_client: Optional[redis_lib.Redis] = Depends(get_redis),
) -> CityOut:
    cache_key = f"city:{slug}:{lang}"

    if redis_client:
        cached = redis_client.get(cache_key)
        if cached:
            item = json.loads(cached)
            return CityOut(**item)

    location = db.query(Location).filter(Location.slug == slug).first()
    if not location:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="City not found")

    # Get translated city name with fallback
    translation = db.query(LocationTranslation).filter(
        LocationTranslation.location_id == location.id,
        LocationTranslation.lang == lang
    ).first()

    # Fallback: translation -> city_en -> city
    city_display = translation.city_name if translation else (location.city_en if location.city_en else location.city)
    city_en_display = location.city_en if location.city_en else location.city

    data = CityOut(
        id=location.id,
        slug=location.slug,
        city=city_display,
        city_en=city_en_display,
        country_code=location.country_code,
        currency=COUNTRY_CURRENCY_MAP.get(location.country_code, DEFAULT_CURRENCY)
    )

    if redis_client:
        redis_client.setex(cache_key, 3600, json.dumps(data.model_dump(), ensure_ascii=False))

    return data
