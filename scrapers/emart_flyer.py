"""이마트 전단 상품 스크래퍼.

Naver Shopping API를 통해 이마트 mallName 상품 중 할인 식품만 추출.
(offline 전단 이미지는 프론트엔드 배너로 별도 링크 제공)
"""
import asyncio
from typing import List
from models import Promotion
from scrapers import naver_api
from scrapers.naver import is_real_food, has_discount_keyword

# 이마트 상품을 찾는 쿼리 (이마트 브랜드·상품 중심)
EMART_QUERIES = [
    "이마트 과일 채소 신선 이번주 행사 할인",
    "이마트 삼겹살 닭고기 정육 이번주 특가",
    "이마트 달걀 우유 두부 이번주 행사",
    "이마트 즉석식품 간편식 냉동 할인 특가",
    "이마트 라면 과자 음료 이번주 행사 할인",
    "노브랜드 이마트 식품 특가 할인",
    "피코크 이마트 간편식 밀키트 특가",
]

# 이마트 mallName 패턴 ('에브리데이', '트레이더스'는 별도 마트)
EMART_MALL_KW    = ("이마트", "SSG", "신세계몰")
EMART_MALL_EXCL  = ("에브리데이", "트레이더스", "백화점", "면세")

# 전단 이미지 전체보기 URL (항상 이번 주 전단)
EMART_FLYER_URL = "https://emartapp.emart.com/webapp/product/flyer?trcknCode=main_leaflet"


def _is_emart_mall(mall: str) -> bool:
    has_kw   = any(k in mall for k in EMART_MALL_KW)
    has_excl = any(k in mall for k in EMART_MALL_EXCL)
    return has_kw and not has_excl


async def fetch() -> List[Promotion]:
    if not naver_api.is_available():
        return []

    batches = await asyncio.gather(
        *[naver_api.search(q, display=30) for q in EMART_QUERIES]
    )
    all_items = [it for sub in batches for it in sub]

    seen_ids: set    = set()
    seen_titles: set = set()
    results: list    = []

    for i, it in enumerate(all_items):
        pid   = it.get("productId", "")
        title = it.get("title", "")
        mall  = it.get("mallName", "")

        if not _is_emart_mall(mall):
            continue
        if not naver_api.is_food_item(it):
            continue
        if not pid:
            continue
        if not is_real_food(title):
            continue
        if not has_discount_keyword(title):
            continue
        if pid in seen_ids or title in seen_titles:
            continue

        seen_ids.add(pid)
        seen_titles.add(title)

        p = naver_api.to_promotion(it, i, force_platform="emart_flyer", force_name="이마트")
        if p:
            rate = naver_api._price_discount_rate(it)
            results.append((rate, p))

    results.sort(key=lambda x: x[0], reverse=True)
    return [p for _, p in results[:25]]
