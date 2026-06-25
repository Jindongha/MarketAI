from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from routers.promotions import router as promotions_router

app = FastAPI(
    title="MarketAI API",
    description="쇼핑몰 할인/프로모션 정보 수집 플랫폼",
    version="0.2.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(promotions_router)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/")
def root():
    return FileResponse("static/index.html")
