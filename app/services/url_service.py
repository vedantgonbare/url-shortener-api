import secrets
import string
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.models.url import URL
from app.schemas.url import URLCreate

def generate_short_code(length: int = 6) -> str:
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

async def create_short_url(db: AsyncSession, url_data: URLCreate) -> URL:
    short_code = url_data.custom_alias or generate_short_code()
    
    db_url = URL(
        original_url=str(url_data.original_url),
        short_code=short_code,
        custom_alias=url_data.custom_alias,
        expires_at=url_data.expires_at
    )

    db.add(db_url)
    await db.commit()
    await db.refresh(db_url)
    return db_url

async def get_url_by_code(db: AsyncSession, short_code: str) -> URL | None:
    result = await db.execute(
        select(URL).where(URL.short_code == short_code, URL.is_active == True)
    )
    return result.scalar_one_or_none()

async def increment_click(db: AsyncSession, short_code: str):
    await db.execute(
        update(URL).where(URL.short_code == short_code).values(
            click_count=URL.click_count + 1
        )
    )
    await db.commit()