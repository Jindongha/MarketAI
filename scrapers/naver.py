from typing import List
from models import Promotion
from scrapers import naver_api

FOOD_QUERIES = [
    "신선 과일 사과 배 포도 특가",
    "신선 채소 양파 감자 당근 할인",
    "정육 돼지고기 삼겹살 닭고기 특가",
    "수산물 생선 고등어 새우 오징어 할인",
    "달걀 우유 두부 신선식품 특가",
    "김치 깍두기 반찬 할인",
    "라면 즉석밥 컵라면 특가",
    "유제품 치즈 요거트 버터 할인",
]

async def fetch() -> List[Promotion]:
    if not naver_api.is_available():
        return []

    all_items = []
    for q in FOOD_QUERIES:
        items = await naver_api.search(q, display=15)
        all_items.extend(items)

    result = []
    seen_ids: set = set()
    seen_titles: set = set()
    for i, it in enumerate(all_items):
        product_id = it.get("productId", "")
        title = it.get("title", "")
        # 식품 카테고리만 허용
        if not naver_api.is_food_item(it):
            continue
        # productId 없으면 스킵 (bot-check URL 방지)
        if not product_id:
            continue
        # 중복 제거
        if product_id in seen_ids or title in seen_titles:
            continue
        seen_ids.add(product_id)
        seen_titles.add(title)
        p = naver_api.to_promotion(it, i)
        if p:
            result.append(p)

    return result[:30]
