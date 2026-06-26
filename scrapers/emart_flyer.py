"""이마트 전단 상품 스크래퍼.

네이버쇼핑 API에서 이마트 몰 상품 우선 + 이마트 PB(노브랜드/피코크) 등
연관 할인 식품으로 채워 개별 상품 카드로 보여준다.
(offline 전단 이미지는 프론트엔드 배너로 별도 링크 제공)
"""
from typing import List
from models import Promotion
from scrapers.mart_products import fetch_mart

EMART_QUERIES = [
    "이마트 과일 채소 신선 이번주 행사 할인",
    "이마트 삼겹살 닭고기 정육 이번주 특가",
    "이마트 달걀 우유 두부 신선 행사 할인",
    "노브랜드 식품 특가 할인",
    "피코크 간편식 밀키트 특가 할인",
    "이마트 라면 과자 음료 행사 할인",
    "이마트 즉석밥 냉동식품 특가 할인",
    "노브랜드 과자 음료 견과 할인 특가",
]

EMART_MALL_KW   = ("이마트", "SSG", "쓱", "신세계", "노브랜드", "피코크")
EMART_MALL_EXCL = ("에브리데이", "트레이더스", "백화점", "면세")

# 전단 이미지 전체보기 URL (항상 이번 주 전단으로 자동 갱신)
EMART_FLYER_URL = "https://emartapp.emart.com/webapp/product/flyer?trcknCode=main_leaflet"


async def fetch() -> List[Promotion]:
    return await fetch_mart(
        platform="emart_flyer",
        platform_name="이마트",
        mall_kw=EMART_MALL_KW,
        mall_excl=EMART_MALL_EXCL,
        queries=EMART_QUERIES,
        limit=25,
    )
