from .categories import router as categories_router
from .cities import router as cities_router
from .providers import router as providers_router
from .leads import router as leads_router
from .events import router as events_router
from .page_events import router as page_events_router

__all__ = [
    "categories_router",
    "cities_router",
    "providers_router",
    "leads_router",
    "events_router",
    "page_events_router",
]
