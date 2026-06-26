from typing import List
from models import Promotion
from scrapers.images import get_image
from scrapers import naver_api

SAMPLE: List[Promotion] = [
    Promotion(id="lotte_1", platform="lotte", platform_name="롯데마트", title="하이트 진로 참이슬 후레쉬 360ml×20병", original_price=36000, sale_price=18000, discount_rate=50, url="https://www.lottemart.com/m/search/listSearchGoodsCount.do?keyword=참이슬", category="주류", badge="1+1", image_url=get_image("음료","")),
    Promotion(id="lotte_2", platform="lotte", platform_name="롯데마트", title="롯데 칸타타 블랙 캔커피 175ml×30캔", original_price=24000, sale_price=16800, discount_rate=30, url="https://www.lottemart.com/m/search/listSearchGoodsCount.do?keyword=칸타타", category="커피", badge="BEST", image_url=get_image("커피","")),
    Promotion(id="lotte_3", platform="lotte", platform_name="롯데마트", title="L물 미네랄워터 2L×24병", original_price=15900, sale_price=10335, discount_rate=35, url="https://www.lottemart.com/m/search/listSearchGoodsCount.do?keyword=L물생수", category="음료", image_url=get_image("물","")),
    Promotion(id="lotte_4", platform="lotte", platform_name="롯데마트", title="풀무원 국산콩 두부 찌개용 3입", original_price=6900, sale_price=4830, discount_rate=30, url="https://www.lottemart.com/m/search/listSearchGoodsCount.do?keyword=풀무원두부", category="간편식", badge="1+1", image_url=get_image("간편식","")),
    Promotion(id="lotte_5", platform="lotte", platform_name="롯데마트", title="곰표 밀가루 중력분 5kg", original_price=7900, sale_price=6320, discount_rate=20, url="https://www.lottemart.com/m/search/listSearchGoodsCount.do?keyword=곰표밀가루", category="소스/양념", image_url=get_image("기름","")),
    Promotion(id="lotte_6", platform="lotte", platform_name="롯데마트", title="남양 초코에몽 240ml×24개", original_price=22800, sale_price=15960, discount_rate=30, url="https://www.lottemart.com/m/search/listSearchGoodsCount.do?keyword=초코에몽", category="유제품", image_url=get_image("음료","")),
]

async def fetch() -> List[Promotion]:
    if naver_api.is_available():
        queries = [
            "롯데 과자 음료 식품 할인",
            "마트 대형 식품 행사 특가",
            "커피 주스 생수 음료 세트 할인",
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
                p = naver_api.to_promotion(it, i, "lotte", "롯데마트")
                if p:
                    result.append(p)
        if len(result) >= 4:
            return result[:12]
    return SAMPLE
