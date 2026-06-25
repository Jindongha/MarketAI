from typing import List
from models import Promotion
from scrapers.images import get_image
from scrapers import naver_api

SAMPLE: List[Promotion] = [
    Promotion(id="emart_1", platform="emart", platform_name="이마트", title="노브랜드 신라면 스타일 라면 5개×6묶음", original_price=16500, sale_price=11550, discount_rate=30, url="https://emart.ssg.com/search.ssg?query=노브랜드라면", category="라면", badge="SSG배송", image_url=get_image("라면","")),
    Promotion(id="emart_2", platform="emart", platform_name="이마트", title="이마트 한돈 삼겹살 500g (냉장)", original_price=18000, sale_price=12600, discount_rate=30, url="https://emart.ssg.com/search.ssg?query=삼겹살", category="육류", badge="오늘드림", image_url=get_image("삼겹살","육류")),
    Promotion(id="emart_3", platform="emart", platform_name="이마트", title="피코크 순두부찌개 밀키트 2인분×3개", original_price=14900, sale_price=10430, discount_rate=30, url="https://emart.ssg.com/search.ssg?query=피코크순두부", category="간편식", image_url=get_image("간편식","")),
    Promotion(id="emart_4", platform="emart", platform_name="이마트", title="노브랜드 생수 2L×6병", original_price=3900, sale_price=2340, discount_rate=40, url="https://emart.ssg.com/search.ssg?query=노브랜드생수", category="음료", badge="BEST", image_url=get_image("물","")),
    Promotion(id="emart_5", platform="emart", platform_name="이마트", title="이마트 유기농 우유 1L×2팩", original_price=7800, sale_price=5850, discount_rate=25, url="https://emart.ssg.com/search.ssg?query=유기농우유", category="유제품", image_url=get_image("유제품","")),
]

async def fetch() -> List[Promotion]:
    if naver_api.is_available():
        queries = [
            "채소 과일 신선 야채 특가",
            "삼겹살 닭고기 육류 냉장 할인",
            "두부 콩나물 계란 신선식품 특가",
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
                p = naver_api.to_promotion(it, i, "emart", "이마트")
                if p:
                    result.append(p)
        if len(result) >= 3:
            return result[:10]
    return SAMPLE
