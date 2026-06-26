"""롯데마트 전단 상품 스크래퍼.

네이버쇼핑 API에서 롯데마트 몰 상품 우선 + 연관 할인 식품으로 채워
개별 상품 카드로 보여준다.
(offline 전단 이미지는 프론트엔드 배너로 별도 링크 제공)
"""
from typing import List
from models import Promotion
from scrapers.mart_products import fetch_mart

LOTTE_QUERIES = [
    "롯데마트 과일 채소 신선 이번주 행사 할인",
    "롯데마트 삼겹살 닭고기 정육 이번주 특가",
    "롯데마트 달걀 우유 두부 신선 행사 할인",
    "롯데마트 라면 과자 음료 행사 할인",
    "롯데마트 수산물 생선 특가 할인",
    "롯데 식품 마트 이번주 행사 1+1 특가",
    "롯데 즉석밥 냉동식품 간편식 특가 할인",
    "마트 신선식품 대용량 할인 특가 행사",
]

LOTTE_MALL_KW   = ("롯데마트", "롯데 마트")
LOTTE_MALL_EXCL = ("롯데온", "롯데백화점", "롯데홈쇼핑", "롯데슈퍼", "롯데닷컴")

# 전단 이미지 전체보기 URL (항상 이번 주 전단으로 자동 갱신)
LOTTE_FLYER_URL = "https://www.mcouponapp.com/lm/401/?from=app_leaflet"


async def fetch() -> List[Promotion]:
    return await fetch_mart(
        platform="lotte_flyer",
        platform_name="롯데마트",
        mall_kw=LOTTE_MALL_KW,
        mall_excl=LOTTE_MALL_EXCL,
        queries=LOTTE_QUERIES,
        limit=25,
    )
