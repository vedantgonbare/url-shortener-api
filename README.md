# 🔗 URL Shortener API

A production-ready URL Shortener REST API built with **FastAPI**, **PostgreSQL**, and **Redis** — similar to Bitly or TinyURL. Features async database access, Redis caching for ultra-fast redirects, click analytics, and custom aliases.

**🌐 Live Demo:** https://url-shortener-api-ycp9.onrender.com/docs

---

## ✨ Features

- **Shorten URLs** — Generate random 6-character short codes instantly
- **Custom Aliases** — Create memorable short links (e.g. `/mygithub`)
- **Fast Redirects** — Redis cache-aside pattern for sub-millisecond lookups
- **Click Analytics** — Track how many times each short link is visited
- **Async Architecture** — Fully async with SQLAlchemy + AsyncPG
- **Auto Docs** — Interactive Swagger UI at `/docs`
- **Docker Ready** — Containerized with Docker + docker-compose

---

## 🛠 Tech Stack

| Technology | Version | Purpose |
|---|---|---|
| FastAPI | 0.135.1 | Web framework |
| Uvicorn | 0.41.0 | ASGI server |
| SQLAlchemy | 2.0.48 | Async ORM |
| Alembic | 1.18.4 | Database migrations |
| PostgreSQL | 17 | Primary database |
| AsyncPG | 0.31.0 | Async PostgreSQL driver |
| Redis | 7.3.0 | Caching layer |
| Pydantic | 2.12.5 | Data validation |
| Docker | latest | Containerization |

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/shorten` | Create a short URL |
| `GET` | `/{short_code}` | Redirect to original URL |
| `GET` | `/info/{short_code}` | Get URL details |
| `GET` | `/analytics/{short_code}` | Get click analytics |
| `GET` | `/health` | Health check |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- PostgreSQL
- Redis
- Docker (optional)

### Local Setup

```bash
# Clone the repo
git clone https://github.com/vedantgonbare/url-shortener-api
cd url-shortener-api

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Fill in your DATABASE_URL, REDIS_URL, SECRET_KEY
```

### Run with Docker

```bash
docker-compose up --build
```

API will be available at `http://localhost:8000/docs`

### Run without Docker

```bash
# Apply database migrations
alembic upgrade head

# Start the server
uvicorn app.main:app --reload
```

---

## ⚙️ Environment Variables

Create a `.env` file in the root directory:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/urlshortener
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-secret-key
ALGORITHM=HS256
```

---

## 📁 Project Structure

```
url-shortener-api/
├── alembic/               # Database migrations
├── app/
│   ├── api/
│   │   └── urls.py        # API route handlers
│   ├── core/
│   │   └── __init__.py    # App settings
│   ├── db/
│   │   └── database.py    # DB connection & session
│   ├── models/
│   │   └── url.py         # SQLAlchemy table definition
│   ├── schemas/
│   │   └── url.py         # Pydantic request/response models
│   ├── services/
│   │   ├── url_service.py # Core business logic
│   │   └── cache_service.py # Redis caching logic
│   └── main.py            # FastAPI app entry point
├── .env                   # Environment variables (not committed)
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── alembic.ini
```

---

## 🔄 How It Works

### URL Shortening
1. User sends `POST /shorten` with `original_url`
2. API generates a cryptographically secure 6-character short code
3. URL is saved to PostgreSQL
4. Short code is returned to user

### Redirect Flow (Cache-Aside Pattern)
1. User visits `/{short_code}`
2. API checks Redis cache first
3. **Cache HIT** → redirect instantly (< 1ms)
4. **Cache MISS** → query PostgreSQL, save to Redis, redirect
5. Click count incremented on every visit

---

## 📊 Example Usage

**Shorten a URL:**
```bash
curl -X POST https://url-shortener-api-ycp9.onrender.com/shorten \
  -H "Content-Type: application/json" \
  -d '{"original_url": "https://github.com/vedantgonbare"}'
```

**Response:**
```json
{
  "id": 1,
  "original_url": "https://github.com/vedantgonbare",
  "short_code": "66gwDm",
  "custom_alias": null,
  "click_count": 0,
  "is_active": true,
  "created_at": "2026-03-19T07:43:53.855028Z"
}
```

**Use the short link:**
```
https://url-shortener-api-ycp9.onrender.com/66gwDm
→ Redirects to https://github.com/vedantgonbare
```

---

## 🌐 Deployment

Deployed on **Render.com** (Frankfurt — EU Central):
- Web Service: FastAPI + Uvicorn
- Database: PostgreSQL 18 (Render managed)
- Cache: Redis (Upstash)
- Migrations run automatically on every deploy via build command

---

## 👨‍💻 Author

**Vedant Gonbare**  
BSc IT | Mumbai
[GitHub](https://github.com/vedantgonbare)

---



