import json
from typing import Optional

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, distinct
import redis as redis_lib
from pydantic import BaseModel

from apps.api.constants import COUNTRY_CURRENCY_MAP, DEFAULT_CURRENCY
from apps.api.dependencies import get_db, get_redis
from apps.api.models import Location, LocationTranslation, Service, ServiceCity, Lead, Provider
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


class CityStats(BaseModel):
    provider_count: int
    request_count: int
    average_rating: Optional[float]


@router.get("/cities/{city_slug}/stats", response_model=CityStats)
async def get_city_stats(
    city_slug: str,
    db: Session = Depends(get_db),
    redis_client: Optional[redis_lib.Redis] = Depends(get_redis),
) -> CityStats:
    cache_key = f"city_stats:{city_slug}"

    if redis_client:
        cached = redis_client.get(cache_key)
        if cached:
            return CityStats(**json.loads(cached))

    # Check if city exists
    location = db.query(Location).filter(Location.slug == city_slug).first()
    if not location:
        raise HTTPException(status_code=404, detail="City not found")

    # provider_count: COUNT DISTINCT providers that have entries in service_cities table 
    # joining to locations where locations.slug = city_slug
    provider_count = (
        db.query(func.count(distinct(Service.provider_id)))
        .join(ServiceCity, Service.id == ServiceCity.service_id)
        .join(Location, Location.id == ServiceCity.city_id)
        .filter(Location.slug == city_slug)
        .scalar() or 0
    )

    # request_count: COUNT leads where leads.city_id = locations.id AND locations.slug = city_slug
    request_count = (
        db.query(func.count(Lead.id))
        .join(Location, Location.id == Lead.city_id)
        .filter(Location.slug == city_slug)
        .scalar() or 0
    )

    # average_rating: AVG of providers.rating WHERE providers.rating IS NOT NULL and 
    # provider has service in this city; round to 1 decimal; return null if no ratings
    avg_rating = (
        db.query(func.avg(Provider.rating))
        .join(Service, Service.provider_id == Provider.id)
        .join(ServiceCity, ServiceCity.service_id == Service.id)
        .join(Location, Location.id == ServiceCity.city_id)
        .filter(Location.slug == city_slug, Provider.rating.isnot(None))
        .scalar()
    )

    formatted_avg_rating = round(float(avg_rating), 1) if avg_rating is not None else None

    stats = CityStats(
        provider_count=provider_count,
        request_count=request_count,
        average_rating=formatted_avg_rating
    )

    if redis_client:
        redis_client.setex(cache_key, 1800, stats.model_dump_json())

    return stats
