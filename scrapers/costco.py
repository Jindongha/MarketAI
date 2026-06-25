from typing import List
from models import Promotion
from scrapers.images import get_image
from scrapers import naver_api

SAMPLE: List[Promotion] = [
    Promotion(id="costco_1", platform="costco", platform_name="코스트코", title="Kirkland 혼합 견과류 1.13kg", original_price=28900, sale_price=21675, discount_rate=25, url="https://www.costco.co.kr/search#q=견과류&t=All", category="견과류", badge="이달특가", image_url=get_image("견과류","")),
    Promotion(id="costco_2", platform="costco", platform_name="코스트코", title="Kirkland 연어 필레 냉장 1.2kg", original_price=49900, sale_price=37425, discount_rate=25, url="https://www.costco.co.kr/search#q=연어&t=All", category="수산물", badge="이달특가", image_url=get_image("연어","수산물")),
    Promotion(id="costco_3", platform="costco", platform_name="코스트코", title="Kirkland 닭가슴살 로티세리 1.4kg", original_price=18500, sale_price=13875, discount_rate=25, url="https://www.costco.co.kr/search#q=치킨&t=All", category="육류", image_url=get_image("닭","육류")),
    Promotion(id="costco_4", platform="costco", platform_name="코스트코", title="Kirkland 통밀 크래커 1.36kg", original_price=14900, sale_price=10430, discount_rate=30, url="https://www.costco.co.kr/search#q=크래커&t=All", category="스낵", image_url=get_image("과자","")),
    Promotion(id="costco_5", platform="costco", platform_name="코스트코", title="Kirkland 프로틴바 다크초코 30개입", original_price=44900, sale_price=31430, discount_rate=30, url="https://www.costco.co.kr/search#q=프로틴바&t=All", category="간편식", image_url=get_image("과자","")),
]

async def fetch() -> List[Promotion]:
    if naver_api.is_available():
        queries = ["견과류 대용량 혼합 킬컬랜드 특가", "연어 닭가슴살 대용량 냉장 할인"]
        for q in queries:
            items = await naver_api.search(q, display=20)
            result = []
            for i, it in enumerate(items):
                p = naver_api.to_promotion(it, i, "costco", "코스트코")
                if p:
                    result.append(p)
            if len(result) >= 3:
                return result[:5]
    return SAMPLE
