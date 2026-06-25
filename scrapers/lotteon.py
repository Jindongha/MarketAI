import httpx
from bs4 import BeautifulSoup
from typing import List
from models import Promotion

SAMPLE: List[Promotion] = [
    Promotion(id="lotteon_1", platform="lotteon", platform_name="롯데ON", title="롯데제과 빼빼로 초코 47g×20개 세트", original_price=22000, sale_price=13200, discount_rate=40, url="https://www.lotteon.com", category="과자", badge="ON단독"),
    Promotion(id="lotteon_2", platform="lotteon", platform_name="롯데ON", title="롯데 칠성 사이다 355ml×24캔", original_price=28000, sale_price=18200, discount_rate=35, url="https://www.lotteon.com", category="음료"),
    Promotion(id="lotteon_3", platform="lotteon", platform_name="롯데ON", title="롯데면세점 설화수 윤조에센스 60ml", original_price=89000, sale_price=53400, discount_rate=40, url="https://www.lotteon.com", category="뷰티", badge="ON단독"),
    Promotion(id="lotteon_4", platform="lotteon", platform_name="롯데ON", title="롯데호텔 비즈니스룸 1박 패키지", original_price=280000, sale_price=168000, discount_rate=40, url="https://www.lotteon.com", category="여행/숙박"),
    Promotion(id="lotteon_5", platform="lotteon", platform_name="롯데ON", title="롯데백화점 나이키 에어포스1 07", original_price=119000, sale_price=83300, discount_rate=30, url="https://www.lotteon.com", category="패션", badge="BEST"),
]

HEADERS = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15", "Accept-Language": "ko-KR,ko;q=0.9"}

async def fetch() -> List[Promotion]:
    try:
        async with httpx.AsyncClient(timeout=7.0, follow_redirects=True) as c:
            r = await c.get("https://www.lotteon.com/p/display/main/lottemart", headers=HEADERS)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, "lxml")
                items = soup.select(".prod_item")[:5]
                if items:
                    result = []
                    for i, it in enumerate(items):
                        t = it.select_one(".prod_name")
                        if t:
                            result.append(Promotion(id=f"lotteon_r_{i}", platform="lotteon", platform_name="롯데ON", title=t.get_text(strip=True), url="https://www.lotteon.com"))
                    if result:
                        return result
    except Exception:
        pass
    return SAMPLE
