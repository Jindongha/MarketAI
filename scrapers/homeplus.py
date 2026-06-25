from typing import List
from models import Promotion
from scrapers.images import get_image

SAMPLE: List[Promotion] = [
    Promotion(id="homeplus_1", platform="homeplus", platform_name="홈플러스", title="CJ 제일제당 스팸 340g (1+1)", original_price=7900, sale_price=3950, discount_rate=50, url="https://mfront.homeplus.co.kr/search?keyword=스팸", category="통조림", badge="1+1", image_url=get_image("통조림","")),
    Promotion(id="homeplus_2", platform="homeplus", platform_name="홈플러스", title="홈플러스 한돈 목살 500g (냉장)", original_price=14900, sale_price=10430, discount_rate=30, url="https://mfront.homeplus.co.kr/search?keyword=목살", category="육류", badge="당일배송", image_url=get_image("삼겹살","육류")),
    Promotion(id="homeplus_3", platform="homeplus", platform_name="홈플러스", title="서울우유 흰우유 1L×2개 (1+1)", original_price=5400, sale_price=2700, discount_rate=50, url="https://mfront.homeplus.co.kr/search?keyword=서울우유", category="유제품", badge="1+1", image_url=get_image("유제품","")),
    Promotion(id="homeplus_4", platform="homeplus", platform_name="홈플러스", title="농심 신라면 5개입×6묶음 (30개)", original_price=18000, sale_price=12600, discount_rate=30, url="https://mfront.homeplus.co.kr/search?keyword=신라면", category="라면", badge="BEST", image_url=get_image("라면","")),
    Promotion(id="homeplus_5", platform="homeplus", platform_name="홈플러스", title="홈플러스 딸기 500g (국내산)", original_price=12900, sale_price=9030, discount_rate=30, url="https://mfront.homeplus.co.kr/search?keyword=딸기", category="과일", badge="제철", image_url=get_image("딸기","과일")),
]

async def fetch() -> List[Promotion]:
    return SAMPLE
