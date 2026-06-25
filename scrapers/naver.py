import httpx
from bs4 import BeautifulSoup
from typing import List
from models import Promotion

SAMPLE: List[Promotion] = [
    Promotion(id="naver_1", platform="naver", platform_name="네이버쇼핑", title="삼성 비스포크 냉장고 4도어 845L", original_price=3290000, sale_price=2302000, discount_rate=30, url="https://shopping.naver.com", category="가전", badge="플러스회원"),
    Promotion(id="naver_2", platform="naver", platform_name="네이버쇼핑", title="뉴발란스 993 메이드인USA 스니커즈", original_price=329000, sale_price=230300, discount_rate=30, url="https://shopping.naver.com", category="패션"),
    Promotion(id="naver_3", platform="naver", platform_name="네이버쇼핑", title="로레알 파리 앰플 히알루론산 세럼 30ml", original_price=25000, sale_price=15000, discount_rate=40, url="https://shopping.naver.com", category="뷰티", badge="N페이할인"),
    Promotion(id="naver_4", platform="naver", platform_name="네이버쇼핑", title="한샘 리바트 1인 소파 패브릭", original_price=289000, sale_price=202300, discount_rate=30, url="https://shopping.naver.com", category="가구"),
    Promotion(id="naver_5", platform="naver", platform_name="네이버쇼핑", title="파타고니아 다운 재킷 남성용", original_price=399000, sale_price=239400, discount_rate=40, url="https://shopping.naver.com", category="패션", badge="BEST"),
]

HEADERS = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15", "Accept-Language": "ko-KR,ko;q=0.9"}

async def fetch() -> List[Promotion]:
    try:
        async with httpx.AsyncClient(timeout=7.0, follow_redirects=True) as c:
            r = await c.get("https://shopping.naver.com/home/p/index.naver", headers=HEADERS)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, "lxml")
                items = soup.select(".product_item")[:5]
                if items:
                    result = []
                    for i, it in enumerate(items):
                        t = it.select_one(".product_name")
                        if t:
                            result.append(Promotion(id=f"naver_r_{i}", platform="naver", platform_name="네이버쇼핑", title=t.get_text(strip=True), url="https://shopping.naver.com"))
                    if result:
                        return result
    except Exception:
        pass
    return SAMPLE
