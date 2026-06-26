import asyncio
import time
from fastapi import APIRouter, Query
from typing import Optional
from models import PromotionsResponse, StoreGroup, SummaryResponse
from scrapers import kurly, lotte, coupang, ssg
from scrapers import emart, traders, costco, homeplus, emart_everyday, lotteon, toss, eleven, naver
from scrapers import emart_flyer, lotte_flyer

router = APIRouter(prefix="/api/promotions", tags=["promotions"])

_cache: dict = {}
CACHE_TTL = 600  # 10분

PLATFORM_MAP = {
    "kurly": kurly.fetch,
    "lotte": lotte.fetch,
    "ssg": ssg.fetch,
    "emart": emart.fetch,
    "traders": traders.fetch,
    "costco": costco.fetch,
    "homeplus": homeplus.fetch,
    "everyday": emart_everyday.fetch,
    "lotteon": lotteon.fetch,
    "toss": toss.fetch,
    "eleven": eleven.fetch,
    "naver": naver.fetch,
    "emart_flyer": emart_flyer.fetch,
    "lotte_flyer": lotte_flyer.fetch,
    # "coupang": 봇 차단으로 서버 크롤링 불가 — 파트너스 API 키 발급 시 재추가
}

# 전체 보기 화면에 매장별로 묶어서 보여줄 플랫폼 순서.
# (전단 탭은 가격 없는 전단 이미지라 상품 리스트에서 제외)
SUMMARY_PLATFORMS = [
    "naver", "kurly", "emart", "lotte", "ssg",
    "homeplus", "costco", "traders", "everyday", "lotteon", "toss", "eleven",
]
SUMMARY_PER_STORE = 10  # 매장별로 노출할 인기·할인 상품 개수


def _get_cache(key: str):
    if key in _cache:
        data, ts = _cache[key]
        if time.time() - ts < CACHE_TTL:
            return data
    return None


def _set_cache(key: str, data):
    _cache[key] = (data, time.time())


async def _fetch_platform(platform: str):
    """플랫폼 한 곳의 상품 목록을 캐시 우선으로 가져온다.

    개별 탭(get_promotions)과 전체 보기(get_summary)가 같은 캐시를 공유하므로
    한 곳에서 받아오면 다른 곳에서도 즉시 재사용된다.
    """
    raw_key = f"raw:{platform}"
    cached = _cache.get(raw_key)
    if cached:
        items, ts = cached
        if time.time() - ts < CACHE_TTL:
            return items
    items = await PLATFORM_MAP[platform]()
    _cache[raw_key] = (items, time.time())
    return items


def _rank_for_summary(items):
    """할인율 높은 순 → 동률이면 원래(인기/연관도) 순서 유지하여 상위 N개만."""
    # 가격이 있는 상품만 (전단 이미지 카드 등은 제외)
    priced = [it for it in items if it.sale_price]
    pool = priced or items
    ranked = sorted(pool, key=lambda it: it.discount_rate or 0, reverse=True)
    return ranked[:SUMMARY_PER_STORE]


@router.get("", response_model=PromotionsResponse)
async def get_promotions(platform: Optional[str] = Query(default="all")):
    cached = _get_cache(platform)
    if cached:
        return cached

    if platform in PLATFORM_MAP:
        items = await _fetch_platform(platform)
    else:
        results = await asyncio.gather(*[_fetch_platform(p) for p in PLATFORM_MAP])
        seen_titles: set = set()
        items = []
        for group in results:
            for item in group:
                if item.title not in seen_titles:
                    seen_titles.add(item.title)
                    items.append(item)

    response = PromotionsResponse(items=items, total=len(items))
    _set_cache(platform, response)
    return response


@router.get("/summary", response_model=SummaryResponse)
async def get_summary():
    """전체 보기 화면: 각 매장별 제일 할인 많이 하고 인기 있는 상품 묶음."""
    cached = _get_cache("__summary__")
    if cached:
        return cached

    results = await asyncio.gather(
        *[_fetch_platform(p) for p in SUMMARY_PLATFORMS]
    )

    groups = []
    total = 0
    for platform, items in zip(SUMMARY_PLATFORMS, results):
        top = _rank_for_summary(items)
        if not top:
            continue
        groups.append(StoreGroup(
            platform=platform,
            platform_name=top[0].platform_name,
            items=top,
        ))
        total += len(top)

    response = SummaryResponse(groups=groups, total=total)
    _set_cache("__summary__", response)
    return response
