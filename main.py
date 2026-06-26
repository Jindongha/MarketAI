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


@app.get("/api/debug/pipeline")
async def debug_pipeline():
    """각 플랫폼별로 원본 데이터 → 필터 단계별 결과를 보여줌 (실시간 진단용)."""
    from scrapers import naver as naver_scraper
    from scrapers import coupang as coupang_scraper
    from scrapers import emart_flyer, lotte_flyer

    report: dict = {}

    # ---- 네이버: 단계별 필터 추적 ----
    if naver_api.is_available():
        raw = await naver_api.search(naver_scraper.FOOD_QUERIES[0], display=20)
        stages = {"raw": len(raw), "food": 0, "real_food": 0, "discount": 0}
        passed, dropped = [], []
        for it in raw:
            title = it.get("title", "")
            if not naver_api.is_food_item(it):
                continue
            stages["food"] += 1
            if not naver_scraper.is_real_food(title):
                continue
            stages["real_food"] += 1
            if not naver_scraper.has_discount_keyword(title):
                dropped.append(naver_api.clean_title(title))
                continue
            stages["discount"] += 1
            passed.append(naver_api.clean_title(title))
        report["naver"] = {
            "query": naver_scraper.FOOD_QUERIES[0],
            "stages": stages,
            "passed_sample": passed[:8],
            "dropped_no_discount_sample": dropped[:8],
        }
    else:
        report["naver"] = {"status": "NAVER_KEY_NOT_SET"}

    # ---- 쿠팡: 직접 크롤링 HTTP 상태/개수 ----
    try:
        coupang_items = await coupang_scraper.fetch()
        report["coupang"] = {
            "count": len(coupang_items),
            "sample": [{"title": p.title, "price": p.sale_price, "url": p.url[:80]} for p in coupang_items[:5]],
        }
    except Exception as e:
        report["coupang"] = {"error": f"{type(e).__name__}: {e}"}

    # ---- 전단지 ----
    try:
        ef = await emart_flyer.fetch()
        lf = await lotte_flyer.fetch()
        report["flyers"] = {
            "emart_count": len(ef),
            "emart_sample": [{"title": p.title, "img": (p.image_url or "")[:70]} for p in ef[:3]],
            "lotte_count": len(lf),
            "lotte_sample": [{"title": p.title, "img": (p.image_url or "")[:70]} for p in lf[:3]],
        }
    except Exception as e:
        report["flyers"] = {"error": f"{type(e).__name__}: {e}"}

    return report


@app.get("/api/debug/coupang")
async def debug_coupang():
    """쿠팡 직접 크롤링이 차단되는지 HTTP 상태를 확인."""
    import httpx
    from scrapers.coupang import HEADERS, SEARCH_QUERIES
    url = f"https://www.coupang.com/np/search?q={SEARCH_QUERIES[0].replace(' ', '+')}&channel=user"
    try:
        async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as c:
            r = await c.get(url, headers=HEADERS)
            body = r.text
            return {
                "http_status": r.status_code,
                "body_length": len(body),
                "has_product_list": "search-product" in body,
                "looks_blocked": any(w in body for w in ["Access Denied", "차단", "비정상", "robot", "captcha"]),
                "body_head": body[:300],
            }
    except Exception as e:
        return {"error": f"{type(e).__name__}: {e}"}


@app.get("/")
def root():
    return FileResponse("static/index.html")
