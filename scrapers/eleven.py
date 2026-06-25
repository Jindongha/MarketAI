import httpx
from bs4 import BeautifulSoup
from typing import List
from models import Promotion

SAMPLE: List[Promotion] = [
    Promotion(id="11st_1", platform="eleven", platform_name="11번가", title="LG 그램17 2025 인텔 코어 울트라 7", original_price=2190000, sale_price=1533000, discount_rate=30, url="https://www.11st.co.kr", category="컴퓨터", badge="SK페이할인"),
    Promotion(id="11st_2", platform="eleven", platform_name="11번가", title="애플 아이패드 에어 M2 11인치 256GB", original_price=1049000, sale_price=734300, discount_rate=30, url="https://www.11st.co.kr", category="전자기기", badge="오늘드림"),
    Promotion(id="11st_3", platform="eleven", platform_name="11번가", title="다우니 섬유유연제 3.8L (야외건조)", original_price=19900, sale_price=13930, discount_rate=30, url="https://www.11st.co.kr", category="생활용품"),
    Promotion(id="11st_4", platform="eleven", platform_name="11번가", title="이니스프리 그린티 씨드 세럼 80ml", original_price=38000, sale_price=22800, discount_rate=40, url="https://www.11st.co.kr", category="뷰티", badge="BEST"),
    Promotion(id="11st_5", platform="eleven", platform_name="11번가", title="필립스 전동칫솔 시리즈 3000", original_price=89000, sale_price=53400, discount_rate=40, url="https://www.11st.co.kr", category="건강"),
]

HEADERS = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15", "Accept-Language": "ko-KR,ko;q=0.9"}

async def fetch() -> List[Promotion]:
    try:
        async with httpx.AsyncClient(timeout=7.0, follow_redirects=True) as c:
            r = await c.get("https://m.11st.co.kr/", headers=HEADERS)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, "lxml")
                items = soup.select(".prd-item")[:5]
                if items:
                    result = []
                    for i, it in enumerate(items):
                        t = it.select_one(".prd-name")
                        if t:
                            result.append(Promotion(id=f"11st_r_{i}", platform="eleven", platform_name="11번가", title=t.get_text(strip=True), url="https://www.11st.co.kr"))
                    if result:
                        return result
    except Exception:
        pass
    return SAMPLE
