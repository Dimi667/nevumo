import json
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
import redis as redis_lib

from dependencies import get_db, get_redis
from models import Location
from schemas import CitiesResponse, CityOut

router = APIRouter(prefix="/api/v1", tags=["cities"])


@router.get("/cities", response_model=CitiesResponse)
async def list_cities(
    country: str = Query("BG", min_length=2, max_length=2),
    db: Session = Depends(get_db),
    redis_client: Optional[redis_lib.Redis] = Depends(get_redis),
) -> CitiesResponse:
    cache_key = f"cities:{country}"

    if redis_client:
        cached = redis_client.get(cache_key)
        if cached:
            items = json.loads(cached)
            return CitiesResponse(data=[CityOut(**i) for i in items])

    rows = (
        db.query(Location)
        .filter(Location.country_code == country)
        .order_by(Location.city)
        .all()
    )

    data = [CityOut(slug=loc.slug, name=loc.city) for loc in rows]

    if redis_client and data:
        redis_client.setex(cache_key, 3600, json.dumps([d.model_dump() for d in data]))

    return CitiesResponse(data=data)
