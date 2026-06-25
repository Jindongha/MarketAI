import httpx
from typing import List
from models import Promotion

SAMPLE: List[Promotion] = [
    Promotion(id="traders_1", platform="traders", platform_name="트레이더스", title="하림 IFF 닭가슴살 슬라이스 2kg", original_price=22900, sale_price=14885, discount_rate=35, url="https://traders.ssg.com", category="육류", badge="대용량"),
    Promotion(id="traders_2", platform="traders", platform_name="트레이더스", title="코카콜라 500ml × 40캔 (업소용)", original_price=39900, sale_price=27930, discount_rate=30, url="https://traders.ssg.com", category="음료", badge="대용량"),
    Promotion(id="traders_3", platform="traders", platform_name="트레이더스", title="동원참치 150g × 24캔 세트", original_price=36000, sale_price=25200, discount_rate=30, url="https://traders.ssg.com", category="통조림"),
    Promotion(id="traders_4", platform="traders", platform_name="트레이더스", title="아이배냇 분유 800g × 4캔", original_price=98000, sale_price=68600, discount_rate=30, url="https://traders.ssg.com", category="유아"),
    Promotion(id="traders_5", platform="traders", platform_name="트레이더스", title="트레이더스 피자 냉동 4판 세트", original_price=29900, sale_price=20930, discount_rate=30, url="https://traders.ssg.com", category="냉동식품", badge="BEST"),
]

async def fetch() -> List[Promotion]:
    return SAMPLE
