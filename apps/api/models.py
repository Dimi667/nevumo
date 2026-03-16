from sqlalchemy import Column, Integer, String, Float, Boolean
from database import Base

class Lead(Base):
    __tablename__ = "leads"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    client_name = Column(String)
    phone = Column(String)
    service_type = Column(String)
    notes = Column(String)

class Translation(Base):
    __tablename__ = "translations"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    lang = Column(String, index=True)
    key = Column(String, index=True)
    value = Column(String)

class Provider(Base):
    __tablename__ = "providers"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)            
    job_title = Column(String)       
    category = Column(String, nullable=False, default="provider_category_general")
    rating = Column(Float)           
    jobs_completed = Column(Integer) 
    is_verified = Column(Boolean, default=True)
    city = Column(String, nullable=True)
    profile_image_url = Column(String, nullable=True)
    # Новата колона за SEO приятелски URL адреси:
    slug = Column(String, unique=True, index=True, nullable=False)
