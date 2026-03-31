# security.py → Two jobs: hash passwords + create/verify JWT tokens

from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

# CryptContext → tells passlib to use bcrypt algorithm
# bcrypt automatically salts and hashes passwords
# "deprecated=auto" → auto-upgrade old hashes if needed
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__ident="2b")

# ─── PASSWORD FUNCTIONS ───────────────────────────────────────────

def hash_password(password: str) -> str:
    """Take plain password → return bcrypt hash"""
    # Example: "mypassword123" → "$2b$12$abc...xyz" (60 char string)
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check if plain password matches the stored hash"""
    # bcrypt re-hashes and compares → returns True or False
    return pwd_context.verify(plain_password, hashed_password)

# ─── JWT FUNCTIONS ────────────────────────────────────────────────

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT token with user data inside"""
    to_encode = data.copy()
    
    # Set expiry time
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        # Default: 30 minutes from now
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Add expiry to the token payload
    to_encode.update({"exp": expire})
    
    # Sign the token with our secret key
    # jwt.encode → converts dict to encrypted token string
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt

def decode_access_token(token: str) -> Optional[str]:
    """Decode JWT token → return email (or None if invalid)"""
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        # "sub" is standard JWT field for the subject (our user's email)
        email: str = payload.get("sub")
        return email
    except JWTError:
        # Token is invalid or expired
        return None
