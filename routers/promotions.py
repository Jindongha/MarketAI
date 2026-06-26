import asyncio
import time
from fastapi import APIRouter, Query
from typing import Optional
from models import PromotionsResponse
from scrapers import kurly, lotte, coupang, ssg
from scrapers import emart, traders, costco, homeplus, emart_everyday, lotteon, toss, eleven, naver

router = APIRouter(prefix="/api/promotions", tags=["promotions"])

_cache: dict = {}
CACHE_TTL = 600  # 10분

PLATFORM_MAP = {
    "kurly": kurly.fetch,
    "lotte": lotte.fetch,
    "coupang": coupang.fetch,
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
}


def _get_cache(key: str):
    if key in _cache:
        data, ts = _cache[key]
        if time.time() - ts < CACHE_TTL:
            return data
    return None


def _set_cache(key: str, data):
    _cache[key] = (data, time.time())


@router.get("", response_model=PromotionsResponse)
async def get_promotions(platform: Optional[str] = Query(default="all")):
    cached = _get_cache(platform)
    if cached:
        return cached

    if platform in PLATFORM_MAP:
        items = await PLATFORM_MAP[platform]()
    else:
        results = await asyncio.gather(*[fn() for fn in PLATFORM_MAP.values()])
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
