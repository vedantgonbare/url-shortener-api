from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel, EmailStr
from datetime import timedelta

from app.db.database import get_db
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["Authentication"])

# ─── SCHEMAS ──────────────────────────────────────────────────────

class UserRegister(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserResponse(BaseModel):
    id: int
    email: str
    class Config:
        from_attributes = True

# ─── ENDPOINTS ────────────────────────────────────────────────────

@router.post("/register", response_model=UserResponse, status_code=201)
async def register(user_data: UserRegister, db: AsyncSession = Depends(get_db)):
    # select() is the async way to query — replaces db.query()
    result = await db.execute(select(User).where(User.email == user_data.email))
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = User(
        email=user_data.email,
        hashed_password=hash_password(user_data.password)
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


@router.post("/login", response_model=TokenResponse)
async def login(user_data: UserLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == user_data.email))
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    token = create_access_token(data={"sub": user.email})
    return TokenResponse(access_token=token)