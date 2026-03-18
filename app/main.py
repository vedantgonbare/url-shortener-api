from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.urls import router as url_router

app = FastAPI(
    title="URL Shortner API",
    description="A production-ready URL Shortner with analytics",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(url_router, tags=["URLs"])

@app.get("/")
async def root():
    return{"message": "URL Shortner API is running  🚀 "}

@app.get("/health")
async def health_check():
    return{"status": "healthy"}