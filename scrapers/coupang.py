import asyncio
from typing import List
from models import Promotion
from scrapers.images import get_image
from scrapers import naver_api

# 쿠팡이 네이버 쇼핑에 입점한 상품 위주로 검색
COUPANG_QUERIES = [
    "쿠팡 로켓배송 식품 할인 특가",
    "쿠팡 로켓프레시 신선 과일 채소",
    "쿠팡 라면 즉석밥 음료 할인",
    "쿠팡 고기 닭 냉장 특가",
    "쿠팡 달걀 우유 두부 신선",
]

FAKE_FOOD_KEYWORDS = [
    "장난감", "완구", "모형", "소꿉", "역할놀이", "인형",
    "박스세트", "본상품", "바구니", "조화", "조형물",
    "pcs", "PCS",
]

def is_real_food(title: str) -> bool:
    clean = title.replace("<b>", "").replace("</b>", "")
    return not any(kw in clean for kw in FAKE_FOOD_KEYWORDS)

async def fetch() -> List[Promotion]:
    if not naver_api.is_available():
        return []

    results = await asyncio.gather(*[naver_api.search(q, display=20) for q in COUPANG_QUERIES])
    all_items = [item for sublist in results for item in sublist]

    seen_ids: set = set()
    seen_titles: set = set()
    result = []

    for i, it in enumerate(all_items):
        product_id = it.get("productId", "")
        title = it.get("title", "")
        link = it.get("link", "")
        mall = it.get("mallName", "")

        # 쿠팡 판매 상품만
        if "쿠팡" not in mall:
            continue
        if not naver_api.is_food_item(it):
            continue
        if not product_id or not link:
            continue
        if not is_real_food(title):
            continue
        if product_id in seen_ids or title in seen_titles:
            continue

        seen_ids.add(product_id)
        seen_titles.add(title)
        p = naver_api.to_promotion(it, i, force_platform="coupang", force_name="쿠팡")
        if p:
            result.append(p)

    return result[:20]
