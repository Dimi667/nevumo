import json
from typing import Optional

import redis as redis_lib
from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.orm import Session

from apps.api.dependencies import get_db, get_redis
from apps.api.models import Translation

router = APIRouter(tags=["translations"])


@router.get("/translations")
def get_translations(
    lang: str = Query(..., min_length=2, max_length=5),
    namespace: str = Query(..., min_length=1, max_length=50),
    db: Session = Depends(get_db),
    redis_client: Optional[redis_lib.Redis] = Depends(get_redis),
) -> Response:
    cache_key = f"translations:{lang}:{namespace}"

    if redis_client:
        cached = redis_client.get(cache_key)
        if cached:
            return Response(
                content=cached,
                media_type="application/json; charset=utf-8",
            )

    prefix = f"{namespace}."
    rows = (
        db.query(Translation)
        .filter(
            Translation.lang.in_([lang, "en"] if lang != "en" else ["en"]),
            Translation.key.like(f"{prefix}%"),
        )
        .all()
    )

    result: dict[str, str] = {}
    for row in rows:
        if row.lang == "en" and row.key not in result:
            result[row.key] = row.value
        elif row.lang != "en":
            result[row.key] = row.value

    response_data = {"success": True, "data": result}
    json_content = json.dumps(response_data, ensure_ascii=False)

    if redis_client and result:
        redis_client.setex(cache_key, 3600, json_content)

    return Response(
        content=json_content,
        media_type="application/json; charset=utf-8",
    )
