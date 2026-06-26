"""롯데마트 전단 스크래퍼.

롯데마트 공식 '이번주 전단' 페이지에서 전단지 이미지를 추출하고
각 페이지를 상품 카드처럼 표시한다. 서버가 이미지를 가져오지
못하면 공식 뷰어 링크 카드로 폴백한다.
"""
from typing import List
from models import Promotion
from scrapers.flyer_common import fetch_flyer

LOTTE_FLYER_PAGE = "https://www.mcouponapp.com/lm/401/?from=app_leaflet"
LOTTE_FLYER_VIEW = "https://www.mcouponapp.com/lm/401/?from=app_leaflet"
LOTTE_IMG_HOSTS  = ("mcouponapp.com", "image.lottemart.com", "lottemart.com", "lotteon.com")


async def fetch() -> List[Promotion]:
    return await fetch_flyer(
        platform="lotte_flyer",
        platform_name="롯데마트",
        page_url=LOTTE_FLYER_PAGE,
        official_view_url=LOTTE_FLYER_VIEW,
        allow_hosts=LOTTE_IMG_HOSTS,
    )
