from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="MarketAI API",
    description="AI 기반 마케팅 분석 플랫폼",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "MarketAI API 서버가 실행 중입니다.", "status": "ok"}


@app.get("/health")
def health():
    return {"status": "healthy"}
