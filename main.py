import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from routers.promotions import router as promotions_router
from scrapers import naver_api

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


@app.get("/api/debug/naver")
async def debug_naver():
    client_id = os.getenv("NAVER_CLIENT_ID", "")
    client_secret = os.getenv("NAVER_CLIENT_SECRET", "")
    if not client_id or not client_secret:
        return {"status": "NOT_SET", "message": "NAVER_CLIENT_ID 또는 NAVER_CLIENT_SECRET 환경변수 없음"}
    items = await naver_api.search("신라면 할인", display=5)
    if not items:
        return {"status": "API_ERROR", "message": "Naver API 호출 실패 - 키가 잘못됐거나 요청 제한 초과", "client_id_prefix": client_id[:6] + "..."}
    sample = [{"title": it.get("title",""), "mall": it.get("mallName",""), "image": it.get("image","")[:60]} for it in items[:3]]
    return {"status": "OK", "client_id_prefix": client_id[:6] + "...", "sample_results": sample}


@app.get("/")
def root():
    return FileResponse("static/index.html")
