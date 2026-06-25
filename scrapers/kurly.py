import httpx
from typing import List
from models import Promotion
from scrapers.images import get_image
from scrapers import naver_api

SAMPLE: List[Promotion] = [
    Promotion(id="kurly_1", platform="kurly", platform_name="컬리", title="제주 하우스 감귤 3kg (특상품)", original_price=25000, sale_price=15300, discount_rate=39, url="https://www.kurly.com/categories/029", category="과일", badge="BEST", image_url=get_image("감귤","과일")),
    Promotion(id="kurly_2", platform="kurly", platform_name="컬리", title="유기농 닭가슴살 슬라이스 4팩 (500g×4)", original_price=28000, sale_price=19600, discount_rate=30, url="https://www.kurly.com/categories/031", category="육류", badge="친환경", image_url=get_image("닭","육류")),
    Promotion(id="kurly_3", platform="kurly", platform_name="컬리", title="프리미엄 한우 국거리용 600g", original_price=42000, sale_price=31500, discount_rate=25, url="https://www.kurly.com/categories/031", category="육류", image_url=get_image("한우","육류")),
    Promotion(id="kurly_4", platform="kurly", platform_name="컬리", title="무항생제 유정란 30구", original_price=12000, sale_price=10200, discount_rate=15, url="https://www.kurly.com/categories/033", category="달걀", image_url=get_image("달걀","")),
    Promotion(id="kurly_5", platform="kurly", platform_name="컬리", title="컬리 소금빵 10개입 (냉동)", original_price=15000, sale_price=12000, discount_rate=20, url="https://www.kurly.com/categories/036", category="베이커리", badge="NEW", image_url=get_image("빵","베이커리")),
    Promotion(id="kurly_6", platform="kurly", platform_name="컬리", title="샤인머스캣 1kg (국산)", original_price=32000, sale_price=22400, discount_rate=30, url="https://www.kurly.com/categories/029", category="과일", badge="제철", image_url=get_image("포도","과일")),
]

HEADERS = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15", "Accept": "application/json"}

async def fetch() -> List[Promotion]:
    if naver_api.is_available():
        queries = ["유기농 신선 과일 채소 할인", "냉장 신선식품 특가 할인"]
        for q in queries:
            items = await naver_api.search(q, display=20)
            result = []
            for i, it in enumerate(items):
                p = naver_api.to_promotion(it, i, "kurly", "컬리")
                if p:
                    result.append(p)
            if len(result) >= 4:
                return result[:6]
    return SAMPLE
