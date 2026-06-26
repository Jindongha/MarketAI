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

    # ---- 마트 전단 상품 (이마트/롯데마트) ----
    try:
        from scrapers import emart_flyer as ef_mod, lotte_flyer as lf_mod
        # 실제 검색 결과의 mallName 분포를 확인 (필터 튜닝용)
        emart_raw = await naver_api.search(ef_mod.EMART_QUERIES[0], display=20)
        lotte_raw = await naver_api.search(lf_mod.LOTTE_QUERIES[0], display=20)
        ef = await emart_flyer.fetch()
        lf = await lotte_flyer.fetch()
        report["mart_products"] = {
            "emart_final_count": len(ef),
            "emart_final_sample": [{"title": p.title, "price": p.sale_price} for p in ef[:5]],
            "emart_raw_mallNames": sorted({it.get("mallName", "?") for it in emart_raw}),
            "lotte_final_count": len(lf),
            "lotte_final_sample": [{"title": p.title, "price": p.sale_price} for p in lf[:5]],
            "lotte_raw_mallNames": sorted({it.get("mallName", "?") for it in lotte_raw}),
        }
    except Exception as e:
        report["mart_products"] = {"error": f"{type(e).__name__}: {e}"}

    return report


@app.get("/api/debug/flyer")
async def debug_flyer():
    """전단 공식 페이지를 Render가 받아올 수 있는지 (이미지 추출 가능 여부) 진단."""
    import httpx
    from scrapers.flyer_common import HEADERS, _extract_images
    from scrapers.emart_flyer import EMART_FLYER_PAGE, EMART_IMG_HOSTS
    from scrapers.lotte_flyer import LOTTE_FLYER_PAGE, LOTTE_IMG_HOSTS

    out = {}
    for name, url, hosts in [
        ("emart", EMART_FLYER_PAGE, EMART_IMG_HOSTS),
        ("lotte", LOTTE_FLYER_PAGE, LOTTE_IMG_HOSTS),
    ]:
        try:
            async with httpx.AsyncClient(timeout=12.0, follow_redirects=True) as c:
                r = await c.get(url, headers=HEADERS)
                imgs = _extract_images(r.text, hosts) if r.status_code == 200 else []
                out[name] = {
                    "http_status": r.status_code,
                    "body_length": len(r.text),
                    "images_extracted": len(imgs),
                    "image_sample": imgs[:5],
                }
        except Exception as e:
            out[name] = {"error": f"{type(e).__name__}: {e}"}
    return out


@app.get("/")
def root():
    return FileResponse("static/index.html")
