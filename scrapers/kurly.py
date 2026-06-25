import httpx
from typing import List
from models import Promotion
from scrapers.images import get_image
from scrapers import naver_api

SAMPLE: List[Promotion] = [
    Promotion(id="kurly_1", platform="kurly", platform_name="컬리", title="제주 하우스 감귤 3kg (특상품)", original_price=25000, sale_price=15300, discount_rate=39, url="https://www.kurly.com/categories/029", category="과일", badge="BEST", image_url=get_image("감귤","과일")),
    Promotion(id="kurly_2", platform="kurly", platform_name="컬리", title="유기농 닭가슴살 슬라이스 4팩 (500g×4)", original_price=28000, sale_price=19600, discount_rate=30, url="https://www.kurly.com/categories/031", category="육류", badge="친환경", image_url=get_image("닭","육류")),
    Promotion(id="kurly_3", platform="kurly", platform_name="컬리", title="프리미엄 한우 국거리용 600g", original_price=42000, sale_price=31500, discount_rate=25, url="https://www.kurly.com/categories/031", category="육류", image_url=get_image("한우","육류")),
    Promotion(id="kurly_4", platform="kurly", platform_name="컬리", title="무항생제 유정란 30구", original_price=12000, sale_price=10200, discount_rate=15, url="https://www.kurly.com/categories/033", category="달걀", image_url=get_image("달걀","")),
    Promotion(id="kurly_5", platform="kurly", platform_name="컬리", title="컬리 소금빵 10개입 (냉동)", original_price=15000, sale_price=12000, discount_rate=20, url="https://www.kurly.com/categories/036", category="베이커리", badge="NEW", image_url=get_image("빵","베이커리")),
    Promotion(id="kurly_6", platform="kurly", platform_name="컬리", title="샤인머스캣 1kg (국산)", original_price=32000, sale_price=22400, discount_rate=30, url="https://www.kurly.com/categories/029", category="과일", badge="제철", image_url=get_image("포도","과일")),
]

HEADERS = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15", "Accept": "application/json"}

async def fetch() -> List[Promotion]:
    # 1. Naver API
    if naver_api.is_available():
        queries = ["마켓컬리 신선 할인", "컬리 식품 특가"]
        for q in queries:
            items = await naver_api.search(q, display=20)
            result = []
            for i, it in enumerate(items):
                if any(k in it.get("mallName","") for k in ["마켓컬리","컬리"]):
                    p = naver_api.to_promotion(it, i, "kurly", "컬리")
                    if p:
                        result.append(p)
            if len(result) >= 4:
                return result[:6]

    # 2. Direct API
    try:
        async with httpx.AsyncClient(timeout=6.0, follow_redirects=True) as c:
            r = await c.get("https://api.kurly.com/v1/recommendation/products?sort_type=4&per_page=10", headers=HEADERS)
            if r.status_code == 200:
                data = r.json()
                items = data.get("data", {}).get("products", [])
                if items:
                    result = []
                    for i, p in enumerate(items[:6]):
                        orig = p.get("sales_price", 0)
                        sale = p.get("discounted_price", orig)
                        rate = int((orig - sale) / orig * 100) if orig > sale else 0
                        title = p.get("goods_name", "")
                        result.append(Promotion(
                            id=f"kurly_r_{i}", platform="kurly", platform_name="컬리",
                            title=title, image_url=p.get("goods_image") or get_image(title,""),
                            original_price=orig, sale_price=sale, discount_rate=rate,
                            url=f"https://www.kurly.com/goods/{p.get('goods_no','')}",
                            category=p.get("category_name"),
                        ))
                    if result:
                        return result
    except Exception:
        pass

    return SAMPLE
