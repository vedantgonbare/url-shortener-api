from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.schemas.url import URLCreate, URLResponse
from app.services.url_service import create_short_url, get_url_by_code, increment_click
from app.services.cache_service import get_cached_url, cache_url
from datetime import datetime
from slowapi import Limiter
from slowapi.util import get_remote_address
import qrcode
import io
from fastapi.responses import StreamingResponse
from app.core.dependencies import get_current_user
from app.models.user import User
from typing import Optional

#  We recreate the same limiter here with the same key_func
# SlowAPI automatically syncs this with the one in main.py
# via app.state.limiter — they work as one unit
limiter = Limiter(key_func=get_remote_address)

router = APIRouter()

@router.post("/shorten", response_model=URLResponse)
@limiter.limit("5/minute")
async def shorten_url(request: Request, url_data: URLCreate, db: AsyncSession = Depends(get_db)):
    # Extract user from JWT token if present (optional auth)
    current_user = None
    try:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            from app.core.security import decode_access_token
            from sqlalchemy import select
            from app.models.user import User
            email = decode_access_token(token)
            if email:
                result = await db.execute(select(User).where(User.email == email))
                current_user = result.scalar_one_or_none()
    except Exception:
        pass

    user_id = current_user.id if current_user else None
    db_url = await create_short_url(db, url_data, user_id=user_id)
    await cache_url(db_url.short_code, db_url.original_url)
    return db_url

@router.get("/info/{short_code}", response_model=URLResponse)
async def get_url_info(short_code: str, db: AsyncSession = Depends(get_db)):
    db_url = await get_url_by_code(db, short_code)
    if not db_url:
        raise HTTPException(status_code=404, detail="URL not found")
    return db_url

@router.get("/analytics/{short_code}")
async def get_analytics(short_code: str, db: AsyncSession = Depends(get_db)):
    db_url = await get_url_by_code(db, short_code)
    if not db_url:
        raise HTTPException(status_code=404, detail="URL not found")
    
    return {
        "short_code": db_url.short_code,
        "original_url": db_url.original_url,
        "click_count": db_url.click_count,
        "created_at": db_url.created_at,
        "is_active": db_url.is_active,
        "custom_alias": db_url.custom_alias,
        "expires_at": db_url.expires_at
    }

@router.get("/{short_code}")
async def redirect_url(short_code: str, db: AsyncSession = Depends(get_db)):
    cached_url = await get_cached_url(short_code)
    if cached_url:
        await increment_click(db, short_code)
        return RedirectResponse(url=cached_url)

    db_url = await get_url_by_code(db, short_code)
    if not db_url:
        raise HTTPException(status_code=404, detail="URL not found")
    if db_url.expires_at and db_url.expires_at < datetime.now():
        raise HTTPException(status_code=410, detail="URL has expired")

    await cache_url(short_code, db_url.original_url)
    await increment_click(db, short_code)
    return RedirectResponse(url=db_url.original_url)


# 🧠 BASE_URL is the root of your deployed API
# We build the full short URL by combining it with the short_code
# e.g. https://your-api.onrender.com/abc123
BASE_URL = "https://url-shortener-api-ycp9.onrender.com"

@router.get("/qr/{short_code}")
async def generate_qr(short_code: str, db: AsyncSession = Depends(get_db)):
    
    # Step 1: Check if this short_code exists in DB
    db_url = await get_url_by_code(db, short_code)
    if not db_url:
        raise HTTPException(status_code=404, detail="URL not found")

    # Step 2: Build the full shortened URL
    # This is the URL the QR code will point to
    short_url = f"{BASE_URL}/{short_code}"

    # Step 3: Generate the QR code
    # qr.make(fit=True) → auto-sizes the QR code to fit the data
    # box_size=10 → each QR "box" is 10 pixels
    # border=4 → standard QR border (called "quiet zone")
    qr = qrcode.QRCode(box_size=10, border=4)
    qr.add_data(short_url)
    qr.make(fit=True)

    # Step 4: Convert to image
    # fill_color/back_color → black on white (standard QR)
    img = qr.make_image(fill_color="black", back_color="white")

    # Step 5: Save image to memory buffer (not disk!)
    # BytesIO() = a file-like object that lives in RAM
    # img.save(buf) → writes PNG bytes into the buffer
    # buf.seek(0) → rewind to start so we can read it back
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    # Step 6: Return as image response
    # media_type="image/png" tells browser: this is an image
    return StreamingResponse(buf, media_type="image/png")