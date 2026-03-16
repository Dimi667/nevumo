from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Тук насочваме към Docker базата
SQLALCHEMY_DATABASE_URL = "postgresql://nevumo_user:secure_password@127.0.0.1:5432/nevumo_leads"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"options": "-c client_encoding=utf8"}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Lead(Base):
    __tablename__ = "leads"
    id = Column(Integer, primary_key=True, index=True)
    client_name = Column(String, index=True)
    phone = Column(String)
    notes = Column(Text, nullable=True) 
    service_type = Column(String)

def init_db():
    Base.metadata.create_all(bind=engine)