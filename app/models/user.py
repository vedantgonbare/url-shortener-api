from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base

class User(Base):
    __tablename__ = "users"

    # Primary key — every table needs one
    # autoincrement=True means DB auto-assigns 1, 2, 3...
    id = Column(Integer, primary_key=True, autoincrement=True)

    # unique=True → no two users can have same email
    # index=True → makes searching by email fast
    email = Column(String, unique=True, index=True, nullable=False)

    # We never store plain passwords!
    # Always store hashed password (bcrypt)
    hashed_password = Column(String, nullable=False)

    # server_default=func.now() → DB sets this automatically
    # when a new row is inserted
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # relationship() → SQLAlchemy ORM magic
    # This lets you do user.urls → get all URLs for this user
    # back_populates="owner" → the URL model will have an "owner" attribute
    # urls = relationship("URL", back_populates="owner")