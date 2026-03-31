# 🔗 LinkSnap — URL Shortener with Analytics

> Create short, powerful links with real-time analytics, QR codes, and a beautiful dashboard.

**Live Demo:** [url-shortener-frontend-khaki.vercel.app](https://url-shortener-frontend-khaki.vercel.app)

---

## ✨ Features

- **URL Shortening** — Instantly shorten any long URL with a custom or auto-generated short code
- **QR Code Generation** — Automatically generate a scannable QR code for every shortened link
- **Real-time Analytics** — Track clicks, active links, and usage stats from your dashboard
- **User Authentication** — Secure JWT-based register/login system
- **Personal Dashboard** — Manage all your links in one place
- **Copy to Clipboard** — One-click copy for shortened URLs
- **Redis Caching** — Fast URL redirects powered by Redis cache
- **Rate Limiting** — API protection with SlowAPI rate limiting

---

## 🛠️ Tech Stack

### Frontend
| Technology | Purpose |
|---|---|
| React.js | UI framework |
| Axios | HTTP client |
| React Router | Client-side routing |
| Vercel | Deployment & hosting |

### Backend
| Technology | Purpose |
|---|---|
| FastAPI | REST API framework |
| PostgreSQL | Primary database |
| SQLAlchemy | ORM |
| Alembic | Database migrations |
| Redis | Caching layer |
| JWT (python-jose) | Authentication tokens |
| bcrypt / passlib | Password hashing |
| qrcode | QR code generation |
| Render | Deployment & hosting |

---

## 🏗️ Architecture

```
┌─────────────────┐         ┌─────────────────┐
│                 │  HTTPS  │                 │
│  React Frontend │ ──────► │  FastAPI Backend │
│  (Vercel)       │         │  (Render)        │
│                 │         │                 │
└─────────────────┘         └────────┬────────┘
                                      │
                          ┌───────────┼───────────┐
                          │           │           │
                    ┌─────▼─────┐ ┌───▼───┐  ┌───▼──────┐
                    │ PostgreSQL│ │ Redis │  │ QR Code  │
                    │ Database  │ │ Cache │  │ Generator│
                    └───────────┘ └───────┘  └──────────┘
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL
- Redis

### Backend Setup

```bash
# Clone the repo
git clone https://github.com/vedantgonbare/url-shortener-api
cd url-shortener-api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your DATABASE_URL, SECRET_KEY, REDIS_URL

# Run database migrations
alembic upgrade head

# Start the server
uvicorn app.main:app --reload
```

### Frontend Setup

```bash
# Clone the repo
git clone https://github.com/vedantgonbare/url-shortener-frontend
cd url-shortener-frontend

# Install dependencies
npm install

# Set up environment variables
echo "REACT_APP_API_URL=http://localhost:8000" > .env

# Start the app
npm start
```

---

## 📡 API Endpoints

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | `/auth/register` | Register new user | ❌ |
| POST | `/auth/login` | Login & get JWT token | ❌ |
| POST | `/shorten` | Shorten a URL | ✅ |
| GET | `/{short_code}` | Redirect to original URL | ❌ |
| GET | `/info/{short_code}` | Get URL info | ❌ |
| GET | `/analytics/{short_code}` | Get click analytics | ✅ |
| GET | `/dashboard/` | Get user dashboard | ✅ |

Full API docs available at: [`/docs`](https://url-shortener-api-ycp9.onrender.com/docs)

---

## 🌐 Deployment

| Service | Platform | URL |
|---|---|---|
| Frontend | Vercel | [url-shortener-frontend-khaki.vercel.app](https://url-shortener-frontend-khaki.vercel.app) |
| Backend API | Render | [url-shortener-api-ycp9.onrender.com](https://url-shortener-api-ycp9.onrender.com) |

---

## 📸 Screenshots

### Landing Page
> Clean, modern landing page with instant URL shortening

### Dashboard
> Personal dashboard showing all links, click stats, and QR codes

---

## 🔒 Environment Variables

### Backend (`.env`)
```
DATABASE_URL=postgresql://...
SECRET_KEY=your-secret-key
ALGORITHM=HS256
REDIS_URL=redis://...
```

### Frontend (`.env`)
```
REACT_APP_API_URL=https://url-shortener-api-ycp9.onrender.com
```

---

## 👨‍💻 Author

**Vedant Gonbare**
- GitHub: [@vedantgonbare](https://github.com/vedantgonbare)
- LinkedIn: [linkedin.com/in/vedantgonbare](https://linkedin.com/in/vedantgonbare)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
