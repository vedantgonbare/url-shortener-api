from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.schemas.url import URLCreate, URLResponse
from app.services.url_service import create_short_url, get_url_by_code, increment_click
from app.services.cache_service import get_cached_url, cache_url
from datetime import datetime

router = APIRouter()

@router.post("/shorten", response_model=URLResponse)
async def shorten_url(url_data: URLCreate, db: AsyncSession = Depends(get_db)):
    db_url = await create_short_url(db, url_data)
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