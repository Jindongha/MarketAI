from typing import List
from models import Promotion
from scrapers.images import get_image
from scrapers import naver_api

SAMPLE: List[Promotion] = [
    Promotion(id="traders_1", platform="traders", platform_name="트레이더스", title="하림 IFF 닭가슴살 슬라이스 2kg", original_price=22900, sale_price=14885, discount_rate=35, url="https://traders.ssg.com/search.ssg?query=닭가슴살", category="육류", badge="대용량", image_url=get_image("닭","육류")),
    Promotion(id="traders_2", platform="traders", platform_name="트레이더스", title="동원참치 150g×24캔 세트", original_price=36000, sale_price=25200, discount_rate=30, url="https://traders.ssg.com/search.ssg?query=동원참치", category="통조림", image_url=get_image("통조림","")),
    Promotion(id="traders_3", platform="traders", platform_name="트레이더스", title="코카콜라 250ml×40캔", original_price=39900, sale_price=27930, discount_rate=30, url="https://traders.ssg.com/search.ssg?query=코카콜라", category="음료", badge="대용량", image_url=get_image("음료","")),
    Promotion(id="traders_4", platform="traders", platform_name="트레이더스", title="트레이더스 피자 냉동 4판 세트", original_price=29900, sale_price=20930, discount_rate=30, url="https://traders.ssg.com/search.ssg?query=피자", category="냉동식품", badge="BEST", image_url=get_image("냉동","")),
    Promotion(id="traders_5", platform="traders", platform_name="트레이더스", title="하단 배추김치 3kg (국내산)", original_price=24900, sale_price=17430, discount_rate=30, url="https://traders.ssg.com/search.ssg?query=배추김치", category="김치", image_url=get_image("김치","")),
]

async def fetch() -> List[Promotion]:
    if naver_api.is_available():
        queries = [
            "대용량 묶음 식품 세트 특가",
            "닭가슴살 참치 햄 대용량 할인",
            "생수 콜라 음료 24캔 묶음 특가",
        ]
        all_items = []
        for q in queries:
            items = await naver_api.search(q, display=15)
            all_items.extend(items)
        result = []
        seen = set()
        for i, it in enumerate(all_items):
            title = it.get("title", "")
            if title not in seen:
                seen.add(title)
                p = naver_api.to_promotion(it, i, "traders", "트레이더스")
                if p:
                    result.append(p)
        if len(result) >= 3:
            return result[:10]
    return SAMPLE
