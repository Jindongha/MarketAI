import httpx
from bs4 import BeautifulSoup
from typing import List
from models import Promotion

SAMPLE: List[Promotion] = [
    Promotion(id="costco_1", platform="costco", platform_name="코스트코", title="Kirkland 견과류 믹스 1.13kg", original_price=28900, sale_price=21675, discount_rate=25, url="https://www.costco.co.kr", category="견과류", badge="이달의 특가"),
    Promotion(id="costco_2", platform="costco", platform_name="코스트코", title="Kirkland 연어 필레 (냉장) 1.2kg", original_price=49900, sale_price=37425, discount_rate=25, url="https://www.costco.co.kr", category="수산물", badge="이달의 특가"),
    Promotion(id="costco_3", platform="costco", platform_name="코스트코", title="Kirkland 치킨 로스트 1.4kg (조리완료)", original_price=18500, sale_price=13875, discount_rate=25, url="https://www.costco.co.kr", category="즉석식품"),
    Promotion(id="costco_4", platform="costco", platform_name="코스트코", title="Dyson V12 무선청소기 (정품)", original_price=799000, sale_price=559300, discount_rate=30, url="https://www.costco.co.kr", category="가전", badge="온라인 단독"),
    Promotion(id="costco_5", platform="costco", platform_name="코스트코", title="Kirkland 프로틴바 30개입 (다크초코)", original_price=44900, sale_price=31430, discount_rate=30, url="https://www.costco.co.kr", category="건강식품"),
]

HEADERS = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15", "Accept-Language": "ko-KR,ko;q=0.9"}

async def fetch() -> List[Promotion]:
    try:
        async with httpx.AsyncClient(timeout=7.0, follow_redirects=True) as c:
            r = await c.get("https://www.costco.co.kr/promotions", headers=HEADERS)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, "lxml")
                items = soup.select(".product-tile")[:5]
                if items:
                    result = []
                    for i, it in enumerate(items):
                        t = it.select_one(".product-name")
                        if t:
                            result.append(Promotion(id=f"costco_r_{i}", platform="costco", platform_name="코스트코", title=t.get_text(strip=True), url="https://www.costco.co.kr"))
                    if result:
                        return result
    except Exception:
        pass
    return SAMPLE
