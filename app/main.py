from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.api.urls import router as url_router
from app.api.auth import router as auth_router
from app.api.dashboard import router as dashboard_router

# 🧠 get_remote_address is a function from slowapi
# It extracts the IP address from the incoming request
# This is how the limiter knows WHO is making requests
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="URL Shortner API",
    description="A production-ready URL Shortner with analytics",
    version="1.0.0"
)

# 🧠 We attach the limiter to the app's state
# app.state is a place FastAPI gives you to store
# custom objects that need to be accessible everywhere
app.state.limiter = limiter

# 🧠 This registers a custom error handler
# When rate limit is exceeded, instead of a crash,
# it returns a proper 429 Too Many Requests response
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(url_router, tags=["URLs"])
app.include_router(auth_router)
app.include_router(dashboard_router)

@app.get("/")
async def root():
    return{"message": "URL Shortner API is running 🚀"}

@app.get("/health")
async def health_check():
    return{"status": "healthy"}