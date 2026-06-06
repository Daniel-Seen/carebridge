"""CareBridge Backend — FastAPI Application"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import elders, updates, health
from app.data.database import init_db

app = FastAPI(
    title="CareBridge API",
    description="养老机构家属沟通与每日动态平台",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://daniel-seen.github.io"],
    allow_origin_regex="https://.*\.trycloudflare\.com",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(elders.router, prefix="/api/elders", tags=["老人管理"])
app.include_router(updates.router, prefix="/api/updates", tags=["每日动态"])
app.include_router(health.router, prefix="/api/health", tags=["健康数据"])


@app.on_event("startup")
async def startup():
    await init_db()


@app.get("/api/ping")
async def ping():
    return {"status": "ok", "service": "CareBridge API"}
