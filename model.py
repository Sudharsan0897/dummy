from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from database import Base


class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    branch = Column(String(50), nullable=False)
    team = Column(String(50), nullable=False)
    role = Column(String(20), default="user")
    reset_token = Column(String(255), nullable=True)
    reset_token_expires = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
# -----------------------------------------------------------------------------------------
    # In main.py or main.py (ONCE, at startup) ( try this model later)
    #from models import UserDB  # Import your model FIRST
    # Create tables automatically
    # Base.metadata.create_all(bind=engine)

