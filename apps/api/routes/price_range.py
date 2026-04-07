# -*- coding: utf-8 -*-
import json
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
import redis as redis_lib
from sqlalchemy import func

from dependencies import get_db, get_redis
from models import Service, ServiceCity, Location, Category

router = APIRouter(tags=["price-range"])

# Currency mapping: country_code → currency
CURRENCY_MAP = {
    "PL": "PLN",
    "BG": "EUR",
    "RS": "RSD",
    "CZ": "CZK",
    "GR": "EUR",
}


@router.get("/price-range")
async def get_price_range(
    category_slug: str = Query(..., min_length=1),
    city_slug: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
    redis_client: Optional[redis_lib.Redis] = Depends(get_redis),
):
    """
    Get dynamic price range for a category in a specific city.
    Returns min/max prices, currency, and provider count from real service data.
    """
    cache_key = f"price_range:{category_slug}:{city_slug}"

    # Try to get from cache first
    if redis_client:
        cached = redis_client.get(cache_key)
        if cached:
            return json.loads(cached)

    # Query for price range data
    result = (
        db.query(
            func.min(Service.base_price).label("min_price"),
            func.max(Service.base_price).label("max_price"),
            func.count(func.distinct(Service.provider_id)).label("provider_count"),
            Location.country_code,
        )
        .join(ServiceCity, ServiceCity.service_id == Service.id)
        .join(Location, Location.id == ServiceCity.city_id)
        .join(Category, Category.id == Service.category_id)
        .filter(
            Category.slug == category_slug,
            Location.slug == city_slug,
            Service.base_price.isnot(None),
            Service.price_type != "request",
        )
        .group_by(Location.country_code)
        .first()
    )

    # No results found
    if not result or result.min_price is None:
        response = {"success": True, "data": None}
        if redis_client:
            redis_client.setex(cache_key, 3600, json.dumps(response))
        return response

    # Get currency from country code mapping
    currency = CURRENCY_MAP.get(result.country_code, "EUR")

    response_data = {
        "min": float(result.min_price),
        "max": float(result.max_price),
        "currency": currency,
        "provider_count": result.provider_count,
    }

    response = {"success": True, "data": response_data}

    # Cache the result for 1 hour
    if redis_client:
        redis_client.setex(cache_key, 3600, json.dumps(response))

    return response
