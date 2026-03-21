import os
from typing import Optional

import redis as redis_lib
from sqlalchemy.orm import Session

from database import SessionLocal


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


_redis_client: Optional[redis_lib.Redis] = None

try:
    _redis_client = redis_lib.Redis(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=int(os.getenv("REDIS_PORT", 6379)),
        db=int(os.getenv("REDIS_DB", 0)),
        decode_responses=True,
    )
    _redis_client.ping()
except Exception:
    _redis_client = None


def get_redis() -> Optional[redis_lib.Redis]:
    return _redis_client
