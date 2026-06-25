from typing import List
from models import Promotion
from scrapers.images import get_image
from scrapers import naver_api

SAMPLE: List[Promotion] = [
    Promotion(id="11st_1", platform="eleven", platform_name="11번가", title="CJ 햇반 즉석밥 210g×24개", original_price=32000, sale_price=22400, discount_rate=30, url="https://www.11st.co.kr/browsing/search.tmall?kwd=햇반즉석밥", category="간편식", badge="SK페이", image_url=get_image("간편식","")),
    Promotion(id="11st_2", platform="eleven", platform_name="11번가", title="오뚜기 진라면 순한맛 5개×8묶음", original_price=23000, sale_price=16100, discount_rate=30, url="https://www.11st.co.kr/browsing/search.tmall?kwd=진라면", category="라면", badge="오늘드림", image_url=get_image("라면","")),
    Promotion(id="11st_3", platform="eleven", platform_name="11번가", title="빙그레 바나나맛우유 240ml×24개", original_price=28800, sale_price=20160, discount_rate=30, url="https://www.11st.co.kr/browsing/search.tmall?kwd=바나나우유", category="유제품", badge="BEST", image_url=get_image("유제품","")),
    Promotion(id="11st_4", platform="eleven", platform_name="11번가", title="종가집 배추김치 포기김치 5kg", original_price=49000, sale_price=34300, discount_rate=30, url="https://www.11st.co.kr/browsing/search.tmall?kwd=포기김치", category="김치", image_url=get_image("김치","")),
    Promotion(id="11st_5", platform="eleven", platform_name="11번가", title="동원 참치 라이트스탠다드 150g×24캔", original_price=33600, sale_price=23520, discount_rate=30, url="https://www.11st.co.kr/browsing/search.tmall?kwd=동원참치", category="통조림", image_url=get_image("통조림","")),
]

async def fetch() -> List[Promotion]:
    if naver_api.is_available():
        queries = [
            "즉석밥 햇반 컵라면 즉석식품 특가",
            "CJ 비비고 동원 식품 할인 세트",
            "라면 스낵 과자 음료 대량 특가",
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
                p = naver_api.to_promotion(it, i, "eleven", "11번가")
                if p:
                    result.append(p)
        if len(result) >= 3:
            return result[:10]
    return SAMPLE
