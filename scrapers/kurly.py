import httpx
from typing import List
from models import Promotion

SAMPLE: List[Promotion] = [
    Promotion(id="kurly_1", platform="kurly", platform_name="컬리", title="제주 하우스 감귤 3kg (특상품)", original_price=25000, sale_price=15300, discount_rate=39, url="https://www.kurly.com", category="과일", badge="BEST"),
    Promotion(id="kurly_2", platform="kurly", platform_name="컬리", title="유기농 닭가슴살 4팩 세트 (500g×4)", original_price=28000, sale_price=19600, discount_rate=30, url="https://www.kurly.com", category="육류", badge="친환경"),
    Promotion(id="kurly_3", platform="kurly", platform_name="컬리", title="프리미엄 한우 불고기 600g", original_price=42000, sale_price=31500, discount_rate=25, url="https://www.kurly.com", category="육류"),
    Promotion(id="kurly_4", platform="kurly", platform_name="컬리", title="오가닉 달걀 30구 (무항생제)", original_price=12000, sale_price=10200, discount_rate=15, url="https://www.kurly.com", category="유제품/달걀"),
    Promotion(id="kurly_5", platform="kurly", platform_name="컬리", title="컬리 베이커리 소금빵 10개입", original_price=15000, sale_price=12000, discount_rate=20, url="https://www.kurly.com", category="베이커리", badge="NEW"),
    Promotion(id="kurly_6", platform="kurly", platform_name="컬리", title="샤인머스캣 1kg (국산)", original_price=32000, sale_price=22400, discount_rate=30, url="https://www.kurly.com", category="과일", badge="제철"),
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15",
    "Accept": "application/json",
    "Accept-Language": "ko-KR,ko;q=0.9",
}


async def fetch() -> List[Promotion]:
    try:
        async with httpx.AsyncClient(timeout=6.0, follow_redirects=True) as client:
            resp = await client.get(
                "https://api.kurly.com/v1/recommendation/products?sort_type=4&per_page=10",
                headers=HEADERS,
            )
            if resp.status_code == 200:
                data = resp.json()
                items = data.get("data", {}).get("products", [])
                if items:
                    result = []
                    for i, p in enumerate(items[:6]):
                        original = p.get("sales_price", 0)
                        discounted = p.get("discounted_price", original)
                        rate = int((original - discounted) / original * 100) if original > discounted else 0
                        result.append(Promotion(
                            id=f"kurly_real_{i}",
                            platform="kurly",
                            platform_name="컬리",
                            title=p.get("goods_name", ""),
                            image_url=p.get("goods_image", None),
                            original_price=original,
                            sale_price=discounted,
                            discount_rate=rate,
                            url=f"https://www.kurly.com/goods/{p.get('goods_no', '')}",
                            category=p.get("category_name", None),
                        ))
                    if result:
                        return result
    except Exception:
        pass
    return SAMPLE
