from typing import List
from models import Promotion
from scrapers.images import get_image
from scrapers import naver_api

SAMPLE: List[Promotion] = [
    Promotion(id="toss_1", platform="toss", platform_name="토스쇼핑", title="스타벅스 아메리카노 Tall 10잔 기프티콘", original_price=54500, sale_price=38150, discount_rate=30, url="https://toss.im/shopping", category="커피", badge="토스단독", image_url=get_image("커피","")),
    Promotion(id="toss_2", platform="toss", platform_name="토스쇼핑", title="배달의민족 치킨+피자 5만원권", original_price=50000, sale_price=35000, discount_rate=30, url="https://toss.im/shopping", category="간편식", badge="페이백10%", image_url=get_image("간편식","")),
    Promotion(id="toss_3", platform="toss", platform_name="토스쇼핑", title="이디야 아메리카노 10잔 기프티콘", original_price=40000, sale_price=28000, discount_rate=30, url="https://toss.im/shopping", category="커피", image_url=get_image("커피","")),
    Promotion(id="toss_4", platform="toss", platform_name="토스쇼핑", title="GS25 편의점 1만원 상품권", original_price=10000, sale_price=7000, discount_rate=30, url="https://toss.im/shopping", category="간편식", badge="토스단독", image_url=get_image("과자","")),
    Promotion(id="toss_5", platform="toss", platform_name="토스쇼핑", title="맥도날드 빅맥세트 교환권 5장", original_price=40000, sale_price=28000, discount_rate=30, url="https://toss.im/shopping", category="간편식", badge="무료배송", image_url=get_image("간편식","")),
]

async def fetch() -> List[Promotion]:
    if naver_api.is_available():
        queries = [
            "커피 차 음료 선물세트 특가",
            "건강식품 비타민 영양제 할인",
            "견과류 시리얼 그래놀라 건강 특가",
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
                p = naver_api.to_promotion(it, i, "toss", "토스쇼핑")
                if p:
                    result.append(p)
        if len(result) >= 3:
            return result[:10]
    return SAMPLE
