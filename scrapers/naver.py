import asyncio
import re
from typing import List
from models import Promotion
from scrapers import naver_api

# 인기 할인 식품 검색 쿼리
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
    # 선물세트류 — 할인이 아닌 일반 상품에 '행사'가 붙는 오탐 방지
    "선물세트", "선물용", "기프트", "명절선물", "세트상품", "추석선물", "설날선물",
]

# 명백한 할인 표현 (단어만으로 할인 확정)
# '행사', '이벤트', 단독 '%'는 제외 — 선물세트·'100% 국산' 등 오탐이 많음
DISCOUNT_WORDS = [
    "특가", "세일", "타임딜", "핫딜", "마감임박", "반값",
    "행사가", "할인가", "특별가", "균일가", "떨이", "초특가",
    "1+1", "2+1", "쿠폰할인", "즉시할인", "덤증정",
]

# 'NN% 할인', '할인 NN%', 'NN%↓' 처럼 % 가 할인과 함께 쓰인 경우만 인정
DISCOUNT_PATTERNS = [
    re.compile(r"\d+\s*%\s*(할인|세일|↓|off|OFF|DC|dc)"),
    re.compile(r"(할인|세일)\s*\d+\s*%"),
    re.compile(r"\d+\s*원\s*(할인|↓|→)"),
    re.compile(r"\d+\s*%\s*↓"),
    # '할인'이 점포명(할인점/할인마트)이 아닌 진짜 할인일 때
    re.compile(r"할인(?!점|마트|매장)"),
]

def is_real_food(title: str) -> bool:
    clean = title.replace("<b>", "").replace("</b>", "")
    return not any(kw in clean for kw in FAKE_FOOD_KEYWORDS)

def has_discount_keyword(title: str) -> bool:
    clean = title.replace("<b>", "").replace("</b>", "")
    if any(kw in clean for kw in DISCOUNT_WORDS):
        return True
    return any(p.search(clean) for p in DISCOUNT_PATTERNS)

def get_price_discount_rate(item: dict) -> int:
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

    seen_ids: set = set()
    seen_titles: set = set()
    result = []

    for i, it in enumerate(all_items):
        product_id = it.get("productId", "")
        title = it.get("title", "")
        link = it.get("link", "")

        if not naver_api.is_food_item(it):
            continue
        if not product_id or not link:
            continue
        if not is_real_food(title):
            continue
        # 제목에 할인 키워드가 있는 상품만
        if not has_discount_keyword(title):
            continue
        if product_id in seen_ids or title in seen_titles:
            continue

        seen_ids.add(product_id)
        seen_titles.add(title)

        p = naver_api.to_promotion(it, i, force_platform="naver", force_name="네이버쇼핑")
        if p:
            # 가격 범위로 할인율 계산 가능하면 높은 순으로 정렬용
            rate = get_price_discount_rate(it)
            result.append((rate, p))

    # 가격 할인율 있는 것 먼저, 그 다음 나머지
    result.sort(key=lambda x: x[0], reverse=True)
    return [p for _, p in result[:30]]
