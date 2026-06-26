"""오프라인 마트(이마트/롯데마트) 전단 상품 공통 수집 로직.

네이버쇼핑 API에는 마트가 직접 등록한 상품이 항상 충분히 잡히지 않는다.
그래서 단계적(tier)으로 수집한다:
  Tier 1) mallName이 해당 마트인 진짜 마트몰 상품 (할인 식품)
  Tier 2) 부족하면 해당 마트 PB·연관 할인 식품으로 채움 (탭이 비지 않게)
두 tier 모두 식품 + 할인키워드 + 가짜식품 제외 필터를 통과해야 한다.
"""
import asyncio
from typing import List, Tuple
from models import Promotion
from scrapers import naver_api
from scrapers.naver import is_real_food, has_discount_keyword


def _passes_base_filters(it: dict) -> bool:
    title = it.get("title", "")
    if not it.get("productId"):
        return False
    if not naver_api.is_food_item(it):
        return False
    if not is_real_food(title):
        return False
    if not has_discount_keyword(title):
        return False
    return True


def _mall_matches(mall: str, mall_kw: tuple, mall_excl: tuple) -> bool:
    return any(k in mall for k in mall_kw) and not any(k in mall for k in mall_excl)


async def fetch_mart(
    platform: str,
    platform_name: str,
    mall_kw: tuple,
    mall_excl: tuple,
    queries: List[str],
    limit: int = 25,
) -> List[Promotion]:
    if not naver_api.is_available():
        return []

    batches = await asyncio.gather(
        *[naver_api.search(q, display=30) for q in queries]
    )
    all_items = [it for sub in batches for it in sub]

    seen_ids: set = set()
    seen_titles: set = set()
    tier1: List[Tuple[int, Promotion]] = []  # 진짜 마트몰 상품
    tier2: List[Tuple[int, Promotion]] = []  # 연관 할인 식품 (폴백)

    for i, it in enumerate(all_items):
        if not _passes_base_filters(it):
            continue
        pid = it.get("productId", "")
        title = it.get("title", "")
        if pid in seen_ids or title in seen_titles:
            continue
        seen_ids.add(pid)
        seen_titles.add(title)

        p = naver_api.to_promotion(it, i, force_platform=platform, force_name=platform_name)
        if not p:
            continue
        rate = naver_api._price_discount_rate(it)
        if _mall_matches(it.get("mallName", ""), mall_kw, mall_excl):
            tier1.append((rate, p))
        else:
            tier2.append((rate, p))

    tier1.sort(key=lambda x: x[0], reverse=True)
    tier2.sort(key=lambda x: x[0], reverse=True)

    merged = [p for _, p in tier1]
    if len(merged) < limit:
        merged += [p for _, p in tier2[: limit - len(merged)]]
    return merged[:limit]
