from typing import List
from models import Promotion
from scrapers.images import get_image

SAMPLE: List[Promotion] = [
    Promotion(id="11st_1", platform="eleven", platform_name="11번가", title="CJ 햇반 즉석밥 210g×24개", original_price=32000, sale_price=22400, discount_rate=30, url="https://www.11st.co.kr/browsing/search.tmall?kwd=햇반", category="간편식", badge="SK페이", image_url=get_image("간편식","")),
    Promotion(id="11st_2", platform="eleven", platform_name="11번가", title="오뚜기 진라면 순한맛 5개×8묶음", original_price=23000, sale_price=16100, discount_rate=30, url="https://www.11st.co.kr/browsing/search.tmall?kwd=오뚜기라면", category="라면", badge="오늘드림", image_url=get_image("라면","")),
    Promotion(id="11st_3", platform="eleven", platform_name="11번가", title="다우니 섬유유연제 야외건조 3.8L×2개", original_price=39800, sale_price=23880, discount_rate=40, url="https://www.11st.co.kr/browsing/search.tmall?kwd=다우니", category="생활용품", image_url=get_image("음료","")),
    Promotion(id="11st_4", platform="eleven", platform_name="11번가", title="빙그레 바나나맛우유 240ml×24개", original_price=28800, sale_price=20160, discount_rate=30, url="https://www.11st.co.kr/browsing/search.tmall?kwd=바나나우유", category="유제품", badge="BEST", image_url=get_image("유제품","")),
    Promotion(id="11st_5", platform="eleven", platform_name="11번가", title="종가집 배추김치 포기김치 5kg", original_price=49000, sale_price=34300, discount_rate=30, url="https://www.11st.co.kr/browsing/search.tmall?kwd=포기김치", category="김치", image_url=get_image("김치","")),
]

async def fetch() -> List[Promotion]:
    return SAMPLE
