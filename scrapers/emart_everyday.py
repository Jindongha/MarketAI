from typing import List
from models import Promotion
from scrapers.images import get_image
from scrapers import naver_api

SAMPLE: List[Promotion] = [
    Promotion(id="everyday_1", platform="everyday", platform_name="이마트에브리데이", title="풀무원 순두부찌개 밀키트 2인분", original_price=4500, sale_price=3150, discount_rate=30, url="https://eeveryday.ssg.com/search.ssg?query=순두부찌개", category="간편식", badge="근거리", image_url=get_image("간편식","")),
    Promotion(id="everyday_2", platform="everyday", platform_name="이마트에브리데이", title="에브리데이 새벽 샐러드 혼합 250g", original_price=3900, sale_price=2730, discount_rate=30, url="https://eeveryday.ssg.com/search.ssg?query=샐러드", category="채소", image_url=get_image("채소","")),
    Promotion(id="everyday_3", platform="everyday", platform_name="이마트에브리데이", title="매일유업 바나나맛우유 200ml×6개", original_price=5400, sale_price=3780, discount_rate=30, url="https://eeveryday.ssg.com/search.ssg?query=바나나우유", category="유제품", image_url=get_image("유제품","")),
    Promotion(id="everyday_4", platform="everyday", platform_name="이마트에브리데이", title="CJ 고메 소시지 380g (1+1)", original_price=5900, sale_price=2950, discount_rate=50, url="https://eeveryday.ssg.com/search.ssg?query=소시지", category="육류", badge="1+1", image_url=get_image("삼겹살","육류")),
    Promotion(id="everyday_5", platform="everyday", platform_name="이마트에브리데이", title="노브랜드 배추김치 500g", original_price=5900, sale_price=4130, discount_rate=30, url="https://eeveryday.ssg.com/search.ssg?query=배추김치", category="김치", image_url=get_image("김치","")),
]

async def fetch() -> List[Promotion]:
    if naver_api.is_available():
        queries = [
            "편의점 간편식 샐러드 할인",
            "도시락 김밥 컵라면 간편 특가",
            "냉장 반찬 나물 신선 할인",
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
                p = naver_api.to_promotion(it, i, "everyday", "이마트에브리데이")
                if p:
                    result.append(p)
        if len(result) >= 3:
            return result[:10]
    return SAMPLE
