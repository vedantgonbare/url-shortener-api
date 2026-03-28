from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from app.db.database import Base
from sqlalchemy.orm import relationship

class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, nullable=False)
    short_code = Column(String, unique=True, index=True, nullable=False)
    custom_alias = Column(String, unique=True, index=True, nullable=True)
    is_active = Column(Boolean, default=True)
    click_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=True)


# 🧠 ForeignKey("users.id") → links this column to the id column
# in the users table. nullable=True → URLs can exist WITHOUT a user
# (anonymous URLs still work)
user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

# 🧠 This is the other side of the relationship
# back_populates="urls" → matches the "urls" in User model
# This lets you do url.owner → get the user who created this URL
# owner = relationship("User", back_populates="urls")