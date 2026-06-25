from typing import List
from models import Promotion
from scrapers.images import get_image

SAMPLE: List[Promotion] = [
    Promotion(id="coupang_1", platform="coupang", platform_name="쿠팡", title="동서 맥심 모카골드 커피믹스 180개입", original_price=32000, sale_price=23900, discount_rate=25, url="https://www.coupang.com/np/search?q=맥심커피믹스&channel=user", category="커피", badge="로켓배송", image_url=get_image("커피","")),
    Promotion(id="coupang_2", platform="coupang", platform_name="쿠팡", title="농심 신라면 멀티팩 5개×6묶음 (30개)", original_price=21000, sale_price=14700, discount_rate=30, url="https://www.coupang.com/np/search?q=신라면&channel=user", category="라면", badge="로켓배송", image_url=get_image("라면","")),
    Promotion(id="coupang_3", platform="coupang", platform_name="쿠팡", title="제주 삼다수 2L×24병 (업소용)", original_price=22000, sale_price=15400, discount_rate=30, url="https://www.coupang.com/np/search?q=삼다수&channel=user", category="음료", badge="로켓배송", image_url=get_image("물","")),
    Promotion(id="coupang_4", platform="coupang", platform_name="쿠팡", title="CJ 비비고 왕교자 만두 1.05kg×2봉", original_price=22800, sale_price=15960, discount_rate=30, url="https://www.coupang.com/np/search?q=비비고만두&channel=user", category="냉동식품", badge="로켓배송", image_url=get_image("만두","냉동")),
    Promotion(id="coupang_5", platform="coupang", platform_name="쿠팡", title="매일 바이오 그릭요거트 플레인 500g×2개", original_price=12800, sale_price=8960, discount_rate=30, url="https://www.coupang.com/np/search?q=그릭요거트&channel=user", category="유제품", badge="로켓배송", image_url=get_image("유제품","")),
    Promotion(id="coupang_6", platform="coupang", platform_name="쿠팡", title="청정원 맛술 생강&매실 900ml×2개", original_price=9800, sale_price=6860, discount_rate=30, url="https://www.coupang.com/np/search?q=맛술&channel=user", category="소스/양념", image_url=get_image("소스","")),
]

async def fetch() -> List[Promotion]:
    return SAMPLE
