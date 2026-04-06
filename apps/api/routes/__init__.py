from .auth import router as auth_router
from .categories import router as categories_router
from .cities import router as cities_router
from .client import router as client_router
from .providers import router as providers_router
from .leads import router as leads_router
from .events import router as events_router
from .page_events import router as page_events_router
from .provider import router as provider_router
from .reviews import router as reviews_router
from .user import router as user_router

__all__ = [
    "auth_router",
    "categories_router",
    "cities_router",
    "client_router",
    "providers_router",
    "leads_router",
    "events_router",
    "page_events_router",
    "provider_router",
    "reviews_router",
    "user_router",
]
