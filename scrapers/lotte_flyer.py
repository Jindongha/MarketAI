from typing import List
from models import Promotion
from scrapers.flyer_common import fetch_flyer

# 롯데마트 '이번주 스마트전단' 공식 뷰어 (전점 401) — 매주 자동 최신 교체
LOTTE_FLYER_PAGE = "https://www.mcouponapp.com/lm/401/?from=app_leaflet"
LOTTE_OFFICIAL_VIEW = "https://www.mcouponapp.com/lm/401/?from=app_leaflet"
# 롯데마트 스마트전단 이미지 도메인들
LOTTE_IMG_HOSTS = ("mcouponapp.com", "lottemart.com", "coupond.lottemart", "lotte")


async def fetch() -> List[Promotion]:
    return await fetch_flyer(
        platform="lotte_flyer",
        platform_name="롯데마트 전단",
        page_url=LOTTE_FLYER_PAGE,
        official_view_url=LOTTE_OFFICIAL_VIEW,
        allow_hosts=LOTTE_IMG_HOSTS,
    )
