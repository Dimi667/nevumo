import json
from typing import Optional

import redis as redis_lib
from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.orm import Session

from apps.api.dependencies import get_db, get_redis
from apps.api.services.translation_service import get_namespaced_translations

router = APIRouter(tags=["translations"])


@router.get("/{namespace}")
def get_translations(
    namespace: str,
    lang: str = Query(..., min_length=2, max_length=5),
    db: Session = Depends(get_db),
    redis_client: Optional[redis_lib.Redis] = Depends(get_redis),
) -> Response:
    """
    Fetch translations for a specific namespace and language.
    Path: /api/v1/translations/{namespace}?lang={lang}
    """
    result = get_namespaced_translations(db, lang, namespace, redis_client)
    
    return Response(
        content=json.dumps(result, ensure_ascii=False),
        media_type="application/json; charset=utf-8",
    )
