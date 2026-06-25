import httpx
from bs4 import BeautifulSoup
from typing import List
from models import Promotion

SAMPLE: List[Promotion] = [
    Promotion(id="lotte_1", platform="lotte", platform_name="롯데마트", title="하이트 진로 소주 360ml × 20병 (1+1)", original_price=36000, sale_price=18000, discount_rate=50, url="https://www.lottemart.com", category="주류", badge="1+1"),
    Promotion(id="lotte_2", platform="lotte", platform_name="롯데마트", title="나이키 에어맥스 SC 런닝화", original_price=109000, sale_price=65400, discount_rate=40, url="https://www.lottemart.com", category="패션"),
    Promotion(id="lotte_3", platform="lotte", platform_name="롯데마트", title="롯데 칸타타 블랙 캔커피 175ml × 30캔", original_price=24000, sale_price=16800, discount_rate=30, url="https://www.lottemart.com", category="음료", badge="BEST"),
    Promotion(id="lotte_4", platform="lotte", platform_name="롯데마트", title="L물 미네랄워터 2L × 24병", original_price=15900, sale_price=10335, discount_rate=35, url="https://www.lottemart.com", category="음료"),
    Promotion(id="lotte_5", platform="lotte", platform_name="롯데마트", title="곰표 밀가루 중력분 5kg", original_price=7900, sale_price=6320, discount_rate=20, url="https://www.lottemart.com", category="식재료"),
    Promotion(id="lotte_6", platform="lotte", platform_name="롯데마트", title="풀무원 국산 두부 찌개용 3입 세트", original_price=6900, sale_price=4830, discount_rate=30, url="https://www.lottemart.com", category="두부/콩나물", badge="1+1"),
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15",
    "Accept": "text/html,application/xhtml+xml",
    "Accept-Language": "ko-KR,ko;q=0.9",
}


async def fetch() -> List[Promotion]:
    try:
        async with httpx.AsyncClient(timeout=8.0, follow_redirects=True) as client:
            resp = await client.get("https://www.lottemart.com/display/event/list", headers=HEADERS)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, "lxml")
                items = soup.select(".event-list-item")[:6]
                if items:
                    result = []
                    for i, item in enumerate(items):
                        title_el = item.select_one(".tit")
                        img_el = item.select_one("img")
                        link_el = item.select_one("a")
                        if not title_el:
                            continue
                        result.append(Promotion(
                            id=f"lotte_real_{i}",
                            platform="lotte",
                            platform_name="롯데마트",
                            title=title_el.get_text(strip=True),
                            image_url=img_el.get("src") if img_el else None,
                            url="https://www.lottemart.com" + (link_el.get("href", "") if link_el else ""),
                        ))
                    if result:
                        return result
    except Exception:
        pass
    return SAMPLE
