from typing import List
from models import Promotion
from scrapers.flyer_common import fetch_flyer

# 이마트 '이번주 전단' 공식 뷰어 — 매주 자동으로 최신 전단으로 교체됨
EMART_FLYER_PAGE = "https://eapp.emart.com/leaflet/leafletView_EL.do"
EMART_OFFICIAL_VIEW = "https://emartapp.emart.com/webapp/product/flyer?trcknCode=main_leaflet"
# 이마트 전단 이미지가 올라오는 도메인들
EMART_IMG_HOSTS = ("emart.com", "ssgcdn.com", "shinsegae", "eapp.emart")


async def fetch() -> List[Promotion]:
    return await fetch_flyer(
        platform="emart_flyer",
        platform_name="이마트 전단",
        page_url=EMART_FLYER_PAGE,
        official_view_url=EMART_OFFICIAL_VIEW,
        allow_hosts=EMART_IMG_HOSTS,
    )
