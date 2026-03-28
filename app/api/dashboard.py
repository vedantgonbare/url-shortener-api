from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

from app.db.database import get_db
from app.models.url import URL
from app.models.user import User
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

# ─── RESPONSE SCHEMA ─────────────────────────────────────────────

class URLItem(BaseModel):
    """Shape of each URL in the dashboard response"""
    id: int
    original_url: str
    short_code: str
    custom_alias: Optional[str]
    click_count: int
    is_active: bool
    created_at: datetime
    expires_at: Optional[datetime]

    class Config:
        from_attributes = True

class DashboardResponse(BaseModel):
    """Full dashboard response"""
    email: str
    total_urls: int
    total_clicks: int
    urls: List[URLItem]

# ─── ENDPOINT ────────────────────────────────────────────────────

@router.get("/", response_model=DashboardResponse)
async def get_dashboard(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)  # 👈 This protects the endpoint
):
    """
    Get current user's dashboard.
    Requires: Authorization: Bearer <token> header
    Returns: user's URLs with analytics
    """
    # Get all URLs belonging to this user
    result = await db.execute(
        select(URL).where(URL.user_id == current_user.id)
    )
    urls = result.scalars().all()

    # Calculate totals
    total_clicks = sum(url.click_count for url in urls)

    return DashboardResponse(
        email=current_user.email,
        total_urls=len(urls),
        total_clicks=total_clicks,
        urls=urls
    )