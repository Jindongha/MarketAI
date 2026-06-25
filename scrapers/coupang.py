import httpx
from bs4 import BeautifulSoup
from typing import List
from models import Promotion

SAMPLE: List[Promotion] = [
    Promotion(id="coupang_1", platform="coupang", platform_name="쿠팡", title="삼성 갤럭시 버즈2 프로 무선이어폰", original_price=209000, sale_price=135900, discount_rate=35, url="https://www.coupang.com", category="전자기기", badge="로켓배송"),
    Promotion(id="coupang_2", platform="coupang", platform_name="쿠팡", title="동서 맥심 모카골드 커피믹스 180개입", original_price=32000, sale_price=23900, discount_rate=25, url="https://www.coupang.com", category="식품", badge="로켓배송"),
    Promotion(id="coupang_3", platform="coupang", platform_name="쿠팡", title="마몽드 레드에너지 수분크림 50ml", original_price=38000, sale_price=22800, discount_rate=40, url="https://www.coupang.com", category="뷰티"),
    Promotion(id="coupang_4", platform="coupang", platform_name="쿠팡", title="크리넥스 데코 화장지 30롤", original_price=29900, sale_price=20930, discount_rate=30, url="https://www.coupang.com", category="생활용품", badge="로켓배송"),
    Promotion(id="coupang_5", platform="coupang", platform_name="쿠팡", title="나이키 에어맥스 270 운동화", original_price=159000, sale_price=95400, discount_rate=40, url="https://www.coupang.com", category="패션"),
    Promotion(id="coupang_6", platform="coupang", platform_name="쿠팡", title="비타민C 1000mg 180정 (6개월분)", original_price=25000, sale_price=15000, discount_rate=40, url="https://www.coupang.com", category="건강", badge="로켓배송"),
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Accept": "text/html,application/xhtml+xml",
    "Accept-Language": "ko-KR,ko;q=0.9",
    "Referer": "https://www.coupang.com",
}


async def fetch() -> List[Promotion]:
    try:
        async with httpx.AsyncClient(timeout=8.0, follow_redirects=True) as client:
            resp = await client.get("https://www.coupang.com/np/categories/497", headers=HEADERS)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, "lxml")
                items = soup.select("li.baby-product")[:6]
                if items:
                    result = []
                    for i, item in enumerate(items):
                        name_el = item.select_one(".name")
                        price_el = item.select_one(".price-value")
                        img_el = item.select_one("img")
                        link_el = item.select_one("a")
                        if not name_el:
                            continue
                        result.append(Promotion(
                            id=f"coupang_real_{i}",
                            platform="coupang",
                            platform_name="쿠팡",
                            title=name_el.get_text(strip=True),
                            image_url=img_el.get("src") if img_el else None,
                            sale_price=int(price_el.get_text(strip=True).replace(",", "")) if price_el else None,
                            url="https://www.coupang.com" + (link_el.get("href", "") if link_el else ""),
                            badge="로켓배송",
                        ))
                    if result:
                        return result
    except Exception:
        pass
    return SAMPLE
