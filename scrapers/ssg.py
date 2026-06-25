import httpx
from bs4 import BeautifulSoup
from typing import List
from models import Promotion

SAMPLE: List[Promotion] = [
    Promotion(id="ssg_1", platform="ssg", platform_name="SSG", title="이마트 미국산 프라임 등심 1kg", original_price=58000, sale_price=40600, discount_rate=30, url="https://www.ssg.com", category="육류", badge="쓱배송"),
    Promotion(id="ssg_2", platform="ssg", platform_name="SSG", title="비비고 왕교자 만두 2.1kg", original_price=19800, sale_price=12870, discount_rate=35, url="https://www.ssg.com", category="냉동식품", badge="쓱배송"),
    Promotion(id="ssg_3", platform="ssg", platform_name="SSG", title="오뚜기 3분 카레·짜장 혼합 20개", original_price=22000, sale_price=13200, discount_rate=40, url="https://www.ssg.com", category="가공식품"),
    Promotion(id="ssg_4", platform="ssg", platform_name="SSG", title="신세계 선물세트 한과 모음 (명절)", original_price=65000, sale_price=48750, discount_rate=25, url="https://www.ssg.com", category="선물세트", badge="SPECIAL"),
    Promotion(id="ssg_5", platform="ssg", platform_name="SSG", title="스타벅스 보온 텀블러 500ml", original_price=42000, sale_price=33600, discount_rate=20, url="https://www.ssg.com", category="주방용품"),
    Promotion(id="ssg_6", platform="ssg", platform_name="SSG", title="제주 삼다수 2L × 24병", original_price=18900, sale_price=13230, discount_rate=30, url="https://www.ssg.com", category="음료", badge="쓱배송"),
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15",
    "Accept": "text/html,application/xhtml+xml",
    "Accept-Language": "ko-KR,ko;q=0.9",
}


async def fetch() -> List[Promotion]:
    try:
        async with httpx.AsyncClient(timeout=8.0, follow_redirects=True) as client:
            resp = await client.get("https://m.ssg.com/event/eventList.ssg", headers=HEADERS)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, "lxml")
                items = soup.select(".event_item")[:6]
                if items:
                    result = []
                    for i, item in enumerate(items):
                        title_el = item.select_one(".tit")
                        img_el = item.select_one("img")
                        link_el = item.select_one("a")
                        if not title_el:
                            continue
                        result.append(Promotion(
                            id=f"ssg_real_{i}",
                            platform="ssg",
                            platform_name="SSG",
                            title=title_el.get_text(strip=True),
                            image_url=img_el.get("src") if img_el else None,
                            url="https://m.ssg.com" + (link_el.get("href", "") if link_el else ""),
                            badge="쓱배송",
                        ))
                    if result:
                        return result
    except Exception:
        pass
    return SAMPLE
