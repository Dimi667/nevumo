import json
from typing import Optional

import redis as redis_lib
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from dependencies import get_db, get_redis
from models import Translation

router = APIRouter(tags=["translations"])


@router.get("/translations")
def get_translations(
    lang: str = Query(..., min_length=2, max_length=5),
    namespace: str = Query(..., min_length=1, max_length=50),
    db: Session = Depends(get_db),
    redis_client: Optional[redis_lib.Redis] = Depends(get_redis),
) -> dict[str, object]:
    cache_key = f"translations:{lang}:{namespace}"

    if redis_client:
        cached = redis_client.get(cache_key)
        if cached:
            return {"success": True, "data": json.loads(cached)}

    prefix = f"{namespace}."
    rows = (
        db.query(Translation)
        .filter(
            Translation.lang == lang,
            Translation.key.like(f"{prefix}%"),
        )
        .all()
    )

    result: dict[str, str] = {}
    for row in rows:
        short_key = row.key[len(prefix):]
        result[short_key] = row.value

    if not result and lang != "en":
        rows_en = (
            db.query(Translation)
            .filter(
                Translation.lang == "en",
                Translation.key.like(f"{prefix}%"),
            )
            .all()
        )
        for row in rows_en:
            short_key = row.key[len(prefix):]
            result[short_key] = row.value

    if redis_client and result:
        redis_client.setex(cache_key, 3600, json.dumps(result))

    return {"success": True, "data": result}
