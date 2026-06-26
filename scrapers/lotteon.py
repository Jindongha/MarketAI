from typing import List
from models import Promotion
from scrapers.images import get_image
from scrapers import naver_api

SAMPLE: List[Promotion] = [
    Promotion(id="lotteon_1", platform="lotteon", platform_name="롯데ON", title="롯데제과 빼빼로 초코 47g×20개", original_price=22000, sale_price=13200, discount_rate=40, url="https://www.lotteon.com/search/search?query=빼빼로", category="과자", badge="ON단독", image_url=get_image("과자","")),
    Promotion(id="lotteon_2", platform="lotteon", platform_name="롯데ON", title="롯데 칠성 사이다 355ml×24캔", original_price=28000, sale_price=18200, discount_rate=35, url="https://www.lotteon.com/search/search?query=칠성사이다", category="음료", image_url=get_image("음료","")),
    Promotion(id="lotteon_3", platform="lotteon", platform_name="롯데ON", title="롯데햄 의성마늘 로스팜 340g×3개", original_price=21000, sale_price=14700, discount_rate=30, url="https://www.lotteon.com/search/search?query=로스팜", category="통조림", badge="BEST", image_url=get_image("통조림","")),
    Promotion(id="lotteon_4", platform="lotteon", platform_name="롯데ON", title="롯데 초코파이 정 12개입×6박스", original_price=24000, sale_price=16800, discount_rate=30, url="https://www.lotteon.com/search/search?query=초코파이", category="과자", image_url=get_image("과자","")),
    Promotion(id="lotteon_5", platform="lotteon", platform_name="롯데ON", title="롯데삼강 월드콘 아이스크림 6개×4박스", original_price=22000, sale_price=15400, discount_rate=30, url="https://www.lotteon.com/search/search?query=월드콘", category="냉동식품", image_url=get_image("냉동","")),
]

async def fetch() -> List[Promotion]:
    if naver_api.is_available():
        queries = [
            "롯데 과자 초콜릿 사탕 음료 할인",
            "빼빼로 초코파이 사이다 칠성 특가",
            "스낵 과자 세트 선물 할인",
        ]
        all_items = []
        for q in queries:
            items = await naver_api.search(q, display=15)
            all_items.extend(items)
        result = []
        seen = set()
        for i, it in enumerate(all_items):
            title = it.get("title", "")
            if title not in seen:
                seen.add(title)
                p = naver_api.to_promotion(it, i, "lotteon", "롯데ON")
                if p:
                    result.append(p)
        if len(result) >= 3:
            return result[:10]
    return SAMPLE
