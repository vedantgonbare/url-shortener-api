# URL Shortener API 🔗

A production-ready URL shortening service built with **FastAPI**, **PostgreSQL**, and **Redis**.

## Features
- ✅ Shorten any URL with auto-generated or custom alias
- ✅ Redis caching for ultra-fast redirects
- ✅ Click analytics tracking
- ✅ URL expiration support
- ✅ Auto-generated Swagger documentation
- ✅ Dockerized for easy deployment

## Tech Stack
- **FastAPI** — Modern async Python web framework
- **PostgreSQL** — Primary database
- **SQLAlchemy** — Async ORM
- **Alembic** — Database migrations
- **Redis** — Caching layer
- **Docker** — Containerization

## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/shorten` | Create a short URL |
| GET | `/{short_code}` | Redirect to original URL |
| GET | `/info/{short_code}` | Get URL details |
| GET | `/analytics/{short_code}` | Get click analytics |

## Quick Start

### Run locally
```bash
git clone https://github.com/vedantgonbare/url-shortener-api.git
cd url-shortener-api
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Run with Docker
```bash
docker-compose up --build
```

## API Documentation
Once running, visit `http://localhost:8000/docs` for interactive Swagger UI.