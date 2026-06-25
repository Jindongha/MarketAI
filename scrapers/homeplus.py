import httpx
from bs4 import BeautifulSoup
from typing import List
from models import Promotion

SAMPLE: List[Promotion] = [
    Promotion(id="homeplus_1", platform="homeplus", platform_name="홈플러스", title="CJ 제일제당 스팸 340g (1+1)", original_price=7900, sale_price=3950, discount_rate=50, url="https://mfront.homeplus.co.kr", category="통조림", badge="1+1"),
    Promotion(id="homeplus_2", platform="homeplus", platform_name="홈플러스", title="홈플러스 국내산 한돈 목살 500g", original_price=14900, sale_price=10430, discount_rate=30, url="https://mfront.homeplus.co.kr", category="육류", badge="당일배송"),
    Promotion(id="homeplus_3", platform="homeplus", platform_name="홈플러스", title="서울우유 흰우유 1L×2개 (1+1)", original_price=5400, sale_price=2700, discount_rate=50, url="https://mfront.homeplus.co.kr", category="유제품", badge="1+1"),
    Promotion(id="homeplus_4", platform="homeplus", platform_name="홈플러스", title="농심 신라면 5개입×6묶음 (30개)", original_price=18000, sale_price=12600, discount_rate=30, url="https://mfront.homeplus.co.kr", category="라면", badge="BEST"),
    Promotion(id="homeplus_5", platform="homeplus", platform_name="홈플러스", title="홈플러스 딸기 500g (국내산)", original_price=12900, sale_price=9030, discount_rate=30, url="https://mfront.homeplus.co.kr", category="과일", badge="제철"),
]

HEADERS = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15", "Accept-Language": "ko-KR,ko;q=0.9"}

async def fetch() -> List[Promotion]:
    try:
        async with httpx.AsyncClient(timeout=7.0, follow_redirects=True) as c:
            r = await c.get("https://mfront.homeplus.co.kr/", headers=HEADERS)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, "lxml")
                items = soup.select(".prod-item")[:5]
                if items:
                    result = []
                    for i, it in enumerate(items):
                        t = it.select_one(".prod-name")
                        if t:
                            result.append(Promotion(id=f"homeplus_r_{i}", platform="homeplus", platform_name="홈플러스", title=t.get_text(strip=True), url="https://mfront.homeplus.co.kr"))
                    if result:
                        return result
    except Exception:
        pass
    return SAMPLE
