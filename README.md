# URL Shortener API

A URL shortening service built using FastAPI.

## Features
- Generate short URLs
- Redirect to original URL
- URL expiration support
- Click tracking

## Tech Stack
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic

## Run Locally

pip install -r requirements.txt
uvicorn app.main:app --reload
