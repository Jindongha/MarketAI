from typing import List
from models import Promotion
from scrapers.images import get_image
from scrapers import naver_api

SAMPLE: List[Promotion] = [
    Promotion(id="ssg_1", platform="ssg", platform_name="SSG", title="이마트 미국산 프라임 등심 1kg", original_price=58000, sale_price=40600, discount_rate=30, url="https://www.ssg.com/search/search.ssg?query=프라임등심", category="육류", badge="쓱배송", image_url=get_image("한우","육류")),
    Promotion(id="ssg_2", platform="ssg", platform_name="SSG", title="비비고 왕교자 만두 2.1kg", original_price=19800, sale_price=12870, discount_rate=35, url="https://www.ssg.com/search/search.ssg?query=비비고만두", category="냉동식품", badge="쓱배송", image_url=get_image("만두","냉동")),
    Promotion(id="ssg_3", platform="ssg", platform_name="SSG", title="오뚜기 3분 카레·짜장 혼합 20개 세트", original_price=22000, sale_price=13200, discount_rate=40, url="https://www.ssg.com/search/search.ssg?query=오뚜기3분카레", category="간편식", image_url=get_image("간편식","")),
    Promotion(id="ssg_4", platform="ssg", platform_name="SSG", title="서울우유 흰우유 1L×4개", original_price=9200, sale_price=6440, discount_rate=30, url="https://www.ssg.com/search/search.ssg?query=서울우유", category="유제품", badge="쓱배송", image_url=get_image("유제품","")),
    Promotion(id="ssg_5", platform="ssg", platform_name="SSG", title="제주 삼다수 2L×24병", original_price=18900, sale_price=13230, discount_rate=30, url="https://www.ssg.com/search/search.ssg?query=삼다수", category="음료", badge="쓱배송", image_url=get_image("물","")),
    Promotion(id="ssg_6", platform="ssg", platform_name="SSG", title="하나로 국내산 달걀 30구 (특란)", original_price=11500, sale_price=8050, discount_rate=30, url="https://www.ssg.com/search/search.ssg?query=달걀30구", category="달걀", image_url=get_image("달걀","")),
]

async def fetch() -> List[Promotion]:
    if naver_api.is_available():
        items = await naver_api.search("SSG닷컴 신선식품 할인", display=20)
        result = []
        for i, it in enumerate(items):
            if any(k in it.get("mallName","") for k in ["SSG","신세계몰"]):
                p = naver_api.to_promotion(it, i, "ssg", "SSG")
                if p:
                    result.append(p)
        if len(result) >= 4:
            return result[:6]
    return SAMPLE
