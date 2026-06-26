from typing import List
from models import Promotion
from scrapers import naver_api

FOOD_QUERIES = [
    "국내산 사과 배 신선 과일 kg",
    "신선 채소 양파 감자 당근 kg",
    "돼지고기 삼겹살 목살 냉장 g",
    "고등어 갈치 새우 오징어 생선 신선",
    "무항생제 달걀 30구 특가",
    "우유 두부 콩나물 신선식품",
    "배추김치 포기김치 깍두기 kg",
    "농심 신라면 오뚜기 라면 즉석밥",
    "서울우유 요거트 치즈 유제품",
]

# 실제 식품이 아닌 상품 제목 키워드 블랙리스트
FAKE_FOOD_KEYWORDS = [
    "장난감", "완구", "모형", "소꿉", "역할놀이", "인형",
    "박스세트", "본상품", "바구니", "조화", "조형물",
    "pcs", "PCS", "개입 사과 배 오렌지 포도 키위",
    "계절 선물", "수확 계절", "가을 열매",
]

def is_real_food(title: str) -> bool:
    clean = title.replace("<b>", "").replace("</b>", "")
    return not any(kw in clean for kw in FAKE_FOOD_KEYWORDS)

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
        # 장난감/가짜 식품 제거
        if not is_real_food(title):
            continue
        # 중복 제거
        if product_id in seen_ids or title in seen_titles:
            continue
        seen_ids.add(product_id)
        seen_titles.add(title)
        # 모든 아이템을 네이버쇼핑으로 표시 (쿠팡 셀러여도 네이버쇼핑 탭이므로)
        p = naver_api.to_promotion(it, i, force_platform="naver", force_name="네이버쇼핑")
        if p:
            result.append(p)

    return result[:30]
