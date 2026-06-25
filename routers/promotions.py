import asyncio
import time
from fastapi import APIRouter, Query
from typing import Optional
from models import PromotionsResponse
from scrapers import kurly, lotte, coupang, ssg

router = APIRouter(prefix="/api/promotions", tags=["promotions"])

_cache: dict = {}
CACHE_TTL = 1800  # 30분


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

    if platform == "kurly":
        items = await kurly.fetch()
    elif platform == "lotte":
        items = await lotte.fetch()
    elif platform == "coupang":
        items = await coupang.fetch()
    elif platform == "ssg":
        items = await ssg.fetch()
    else:
        results = await asyncio.gather(
            kurly.fetch(),
            lotte.fetch(),
            coupang.fetch(),
            ssg.fetch(),
        )
        items = [item for group in results for item in group]

    response = PromotionsResponse(items=items, total=len(items))
    _set_cache(platform, response)
    return response
