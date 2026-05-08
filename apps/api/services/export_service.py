from datetime import datetime, timezone
from decimal import Decimal
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from apps.api.models import User, Provider, Lead, Service, Review, ConsentLog


def export_user_data(user_id: UUID, db: Session) -> dict:
    """Export all user data for GDPR Article 20 compliance.
    
    Args:
        user_id: The user's UUID
        db: SQLAlchemy database session
        
    Returns:
        Dictionary containing all user data in a structured format
    """
    # Get user profile
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError("User not found")
    
    # Get provider record if exists
    provider = db.query(Provider).filter(Provider.user_id == user_id).first()
    
    # Collect leads where user is client
    leads_as_client = db.query(Lead).filter(Lead.client_id == user_id).all()
    
    # Collect leads where user is provider (via provider record)
    leads_as_provider = []
    if provider:
        leads_as_provider = db.query(Lead).filter(Lead.provider_id == provider.id).all()
    
    # Collect services for provider
    services = []
    if provider:
        services = db.query(Service).filter(Service.provider_id == provider.id).all()
    
    # Collect reviews given by user
    reviews_given = db.query(Review).filter(Review.client_id == user_id).all()
    
    # Collect reviews received by provider
    reviews_received = []
    if provider:
        reviews_received = db.query(Review).filter(Review.provider_id == provider.id).all()
    
    # Collect consent logs (with try/except in case table doesn't exist)
    consent_log = []
    try:
        consent_log = db.query(ConsentLog).filter(ConsentLog.user_id == user_id).all()
    except Exception:
        # Table might not exist yet or other error
        consent_log = []
    
    # Build export data
    export_data = {
        "exported_at": datetime.now(timezone.utc).isoformat(),
        "profile": {
            "id": str(user.id),
            "email": user.email,
            "name": user.name,
            "phone": user.phone,
            "role": user.role,
            "locale": user.locale,
            "country_code": user.country_code,
            "created_at": user.created_at.isoformat() if user.created_at else None,
        },
        "leads_as_client": [
            {
                "id": str(lead.id),
                "category_id": lead.category_id,
                "city_id": lead.city_id,
                "description": lead.description,
                "budget": str(lead.budget) if lead.budget is not None else None,
                "status": lead.status,
                "created_at": lead.created_at.isoformat() if lead.created_at else None,
            }
            for lead in leads_as_client
        ],
        "leads_as_provider": [
            {
                "id": str(lead.id),
                "client_id": str(lead.client_id) if lead.client_id else None,
                "category_id": lead.category_id,
                "city_id": lead.city_id,
                "status": lead.status,
                "created_at": lead.created_at.isoformat() if lead.created_at else None,
            }
            for lead in leads_as_provider
        ],
        "services": [
            {
                "id": str(service.id),
                "title": service.title,
                "description": service.description,
                "price_type": service.price_type,
                "base_price": str(service.base_price) if service.base_price is not None else None,
                "currency": service.currency,
                "created_at": service.created_at.isoformat() if service.created_at else None,
            }
            for service in services
        ],
        "reviews_given": [
            {
                "id": str(review.id),
                "provider_id": str(review.provider_id),
                "rating": review.rating,
                "comment": review.comment,
                "created_at": review.created_at.isoformat() if review.created_at else None,
            }
            for review in reviews_given
        ],
        "reviews_received": [
            {
                "id": str(review.id),
                "client_id": str(review.client_id),
                "rating": review.rating,
                "comment": review.comment,
                "created_at": review.created_at.isoformat() if review.created_at else None,
            }
            for review in reviews_received
        ],
        "consent_log": [
            {
                "id": str(log.id),
                "action": None,  # ConsentLog doesn't have action field
                "categories": log.categories if log.categories else {},
                "ip_hash": log.ip_hash,
                "created_at": log.created_at.isoformat() if log.created_at else None,
            }
            for log in consent_log
        ],
    }
    
    return export_data
