from typing import List
from models import Promotion
from scrapers.images import get_image

SAMPLE: List[Promotion] = [
    Promotion(id="toss_1", platform="toss", platform_name="토스쇼핑", title="스타벅스 아메리카노 Tall 10잔 기프티콘", original_price=54500, sale_price=38150, discount_rate=30, url="https://toss.im/shopping", category="커피", badge="토스단독", image_url=get_image("커피","")),
    Promotion(id="toss_2", platform="toss", platform_name="토스쇼핑", title="배달의민족 치킨+피자 5만원권", original_price=50000, sale_price=35000, discount_rate=30, url="https://toss.im/shopping", category="간편식", badge="페이백10%", image_url=get_image("간편식","")),
    Promotion(id="toss_3", platform="toss", platform_name="토스쇼핑", title="이디야 아메리카노 10잔 기프티콘", original_price=40000, sale_price=28000, discount_rate=30, url="https://toss.im/shopping", category="커피", image_url=get_image("커피","")),
    Promotion(id="toss_4", platform="toss", platform_name="토스쇼핑", title="GS25 편의점 1만원 상품권", original_price=10000, sale_price=7000, discount_rate=30, url="https://toss.im/shopping", category="간편식", badge="토스단독", image_url=get_image("과자","")),
    Promotion(id="toss_5", platform="toss", platform_name="토스쇼핑", title="맥도날드 빅맥세트 교환권 5장", original_price=40000, sale_price=28000, discount_rate=30, url="https://toss.im/shopping", category="간편식", badge="무료배송", image_url=get_image("간편식","")),
]

async def fetch() -> List[Promotion]:
    return SAMPLE
