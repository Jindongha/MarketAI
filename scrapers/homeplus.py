from typing import List
from models import Promotion
from scrapers.images import get_image
from scrapers import naver_api

SAMPLE: List[Promotion] = [
    Promotion(id="homeplus_1", platform="homeplus", platform_name="홈플러스", title="CJ 제일제당 스팸 340g (1+1)", original_price=7900, sale_price=3950, discount_rate=50, url="https://mfront.homeplus.co.kr/search?keyword=스팸", category="통조림", badge="1+1", image_url=get_image("통조림","")),
    Promotion(id="homeplus_2", platform="homeplus", platform_name="홈플러스", title="홈플러스 한돈 목살 500g", original_price=14900, sale_price=10430, discount_rate=30, url="https://mfront.homeplus.co.kr/search?keyword=목살", category="육류", badge="당일배송", image_url=get_image("삼겹살","육류")),
    Promotion(id="homeplus_3", platform="homeplus", platform_name="홈플러스", title="서울우유 흰우유 1L×2개 (1+1)", original_price=5400, sale_price=2700, discount_rate=50, url="https://mfront.homeplus.co.kr/search?keyword=서울우유", category="유제품", badge="1+1", image_url=get_image("유제품","")),
    Promotion(id="homeplus_4", platform="homeplus", platform_name="홈플러스", title="농심 신라면 5개×6묶음 30개입", original_price=18000, sale_price=12600, discount_rate=30, url="https://mfront.homeplus.co.kr/search?keyword=신라면", category="라면", badge="BEST", image_url=get_image("라면","")),
    Promotion(id="homeplus_5", platform="homeplus", platform_name="홈플러스", title="국내산 딸기 500g (제철)", original_price=12900, sale_price=9030, discount_rate=30, url="https://mfront.homeplus.co.kr/search?keyword=딸기", category="과일", badge="제철", image_url=get_image("딸기","과일")),
]

async def fetch() -> List[Promotion]:
    if naver_api.is_available():
        queries = ["1+1 행사 식품 음료 과자", "홈플러스 마트 신선 식품 특가"]
        for q in queries:
            items = await naver_api.search(q, display=20)
            result = []
            for i, it in enumerate(items):
                p = naver_api.to_promotion(it, i, "homeplus", "홈플러스")
                if p:
                    result.append(p)
            if len(result) >= 3:
                return result[:5]
    return SAMPLE
