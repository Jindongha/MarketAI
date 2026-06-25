from typing import List
from models import Promotion

SAMPLE: List[Promotion] = [
    Promotion(id="toss_1", platform="toss", platform_name="토스쇼핑", title="삼성 갤럭시 S25 256GB (토스 단독가)", original_price=1155000, sale_price=809000, discount_rate=30, url="https://toss.im", category="전자기기", badge="토스단독"),
    Promotion(id="toss_2", platform="toss", platform_name="토스쇼핑", title="에어팟 프로 2세대 (USB-C)", original_price=359000, sale_price=251300, discount_rate=30, url="https://toss.im", category="전자기기", badge="페이백10%"),
    Promotion(id="toss_3", platform="toss", platform_name="토스쇼핑", title="다이슨 슈퍼소닉 헤어드라이어", original_price=599000, sale_price=419300, discount_rate=30, url="https://toss.im", category="가전"),
    Promotion(id="toss_4", platform="toss", platform_name="토스쇼핑", title="나이키 줌 페가수스 41 운동화", original_price=149000, sale_price=104300, discount_rate=30, url="https://toss.im", category="패션", badge="무료배송"),
    Promotion(id="toss_5", platform="toss", platform_name="토스쇼핑", title="스타벅스 아메리카노 10잔 기프티콘", original_price=54500, sale_price=38150, discount_rate=30, url="https://toss.im", category="기프티콘", badge="토스단독"),
]

async def fetch() -> List[Promotion]:
    return SAMPLE
