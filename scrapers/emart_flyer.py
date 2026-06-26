"""이마트 전단 스크래퍼.

이마트 공식 '이번주 전단' 페이지에서 전단지 이미지를 추출하고
각 페이지를 상품 카드처럼 표시한다. 서버가 이미지를 가져오지
못하면 공식 뷰어 링크 카드로 폴백한다.
"""
from typing import List
from models import Promotion
from scrapers.flyer_common import fetch_flyer

EMART_FLYER_PAGE = "https://emartapp.emart.com/webapp/product/flyer?trcknCode=main_leaflet"
EMART_FLYER_VIEW = "https://emartapp.emart.com/webapp/product/flyer?trcknCode=main_leaflet"
EMART_IMG_HOSTS  = ("emart.ssg.com", "sitem.ssgcdn.com", "emart.com", "ssg.com")


async def fetch() -> List[Promotion]:
    return await fetch_flyer(
        platform="emart_flyer",
        platform_name="이마트",
        page_url=EMART_FLYER_PAGE,
        official_view_url=EMART_FLYER_VIEW,
        allow_hosts=EMART_IMG_HOSTS,
    )
