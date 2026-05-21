from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from app.config import settings
from app.database import init_db
from app.routers import farmers, recommendations


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Smart Farming API",
    description="AI-powered agricultural recommendations for sustainable farming",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(farmers.router)
app.include_router(recommendations.router)


@app.get("/")
def root():
    return RedirectResponse(url="/docs")


@app.get("/health")
def health():
    return {"status": "ok", "service": "smart-farming-api"}


@app.get("/api/features/roadmap")
def roadmap():
    from app.services.recommendation_service import FUTURE_FEATURES

    return {
        "planned": FUTURE_FEATURES,
        "architecture": "Modular services ready for ML models, IoT MQTT, and i18n",
    }
