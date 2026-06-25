import httpx
from bs4 import BeautifulSoup
from typing import List
from models import Promotion

SAMPLE: List[Promotion] = [
    Promotion(id="emart_1", platform="emart", platform_name="이마트", title="노브랜드 맛동산 스낵 500g", original_price=4500, sale_price=2900, discount_rate=36, url="https://emart.ssg.com", category="스낵", badge="SSG배송"),
    Promotion(id="emart_2", platform="emart", platform_name="이마트", title="이마트 국내산 삼겹살 400g (냉장)", original_price=18000, sale_price=12600, discount_rate=30, url="https://emart.ssg.com", category="육류", badge="오늘드림"),
    Promotion(id="emart_3", platform="emart", platform_name="이마트", title="피코크 냉동 새우볶음밥 450g×3", original_price=14900, sale_price=10430, discount_rate=30, url="https://emart.ssg.com", category="냉동식품"),
    Promotion(id="emart_4", platform="emart", platform_name="이마트", title="노브랜드 생수 2L×6병", original_price=3900, sale_price=2340, discount_rate=40, url="https://emart.ssg.com", category="음료", badge="BEST"),
    Promotion(id="emart_5", platform="emart", platform_name="이마트", title="이마트 유기농 우유 1L×2팩", original_price=7800, sale_price=5850, discount_rate=25, url="https://emart.ssg.com", category="유제품"),
]

HEADERS = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15", "Accept-Language": "ko-KR,ko;q=0.9"}

async def fetch() -> List[Promotion]:
    try:
        async with httpx.AsyncClient(timeout=7.0, follow_redirects=True) as c:
            r = await c.get("https://emart.ssg.com/", headers=HEADERS)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, "lxml")
                items = soup.select(".sale_item")[:5]
                if items:
                    return [Promotion(id=f"emart_r_{i}", platform="emart", platform_name="이마트",
                        title=it.select_one(".tit").get_text(strip=True),
                        url="https://emart.ssg.com") for i, it in enumerate(items) if it.select_one(".tit")]
    except Exception:
        pass
    return SAMPLE
