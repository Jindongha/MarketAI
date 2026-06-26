import asyncio
from typing import List
from models import Promotion
from scrapers import naver_api

# 할인 행사 중인 인기 식품 쿼리
FOOD_QUERIES = [
    "과일 사과 배 신선 할인 행사",
    "채소 양파 감자 신선 특가 행사",
    "삼겹살 목살 닭가슴살 할인 행사",
    "고등어 새우 오징어 생선 할인 특가",
    "달걀 우유 두부 할인 행사",
    "김치 반찬 할인 특가",
    "라면 즉석밥 할인 행사",
    "요거트 치즈 유제품 할인 특가",
    "견과류 아몬드 호두 할인 행사",
]

FAKE_FOOD_KEYWORDS = [
    "장난감", "완구", "모형", "소꿉", "역할놀이", "인형",
    "박스세트", "본상품", "바구니", "조화", "조형물",
    "pcs", "PCS", "개입 사과 배 오렌지 포도 키위",
    "계절 선물", "수확 계절", "가을 열매",
]

MIN_DISCOUNT = 10  # 최소 할인율 (%)

def is_real_food(title: str) -> bool:
    clean = title.replace("<b>", "").replace("</b>", "")
    return not any(kw in clean for kw in FAKE_FOOD_KEYWORDS)

def get_discount_rate(item: dict) -> int:
    lprice = int(item.get("lprice", 0) or 0)
    hprice = int(item.get("hprice", 0) or 0)
    if hprice > lprice > 0:
        return int((hprice - lprice) / hprice * 100)
    return 0

async def fetch() -> List[Promotion]:
    if not naver_api.is_available():
        return []

    results = await asyncio.gather(*[naver_api.search(q, display=20) for q in FOOD_QUERIES])
    all_items = [item for sublist in results for item in sublist]

    discounted = []
    seen_ids: set = set()
    seen_titles: set = set()

    for i, it in enumerate(all_items):
        product_id = it.get("productId", "")
        title = it.get("title", "")

        if not naver_api.is_food_item(it):
            continue
        if not product_id:
            continue
        if not is_real_food(title):
            continue
        if product_id in seen_ids or title in seen_titles:
            continue

        # 실제 할인이 있는 상품만 (hprice > lprice)
        discount = get_discount_rate(it)
        if discount < MIN_DISCOUNT:
            continue

        seen_ids.add(product_id)
        seen_titles.add(title)

        p = naver_api.to_promotion(it, i, force_platform="naver", force_name="네이버쇼핑")
        if p:
            discounted.append((discount, p))

    # 할인율 높은 순 정렬
    discounted.sort(key=lambda x: x[0], reverse=True)
    return [p for _, p in discounted[:30]]
