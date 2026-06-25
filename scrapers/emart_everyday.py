from typing import List
from models import Promotion

SAMPLE: List[Promotion] = [
    Promotion(id="everyday_1", platform="everyday", platform_name="이마트 에브리데이", title="풀무원 순두부찌개 2인분 (간편조리)", original_price=4500, sale_price=3150, discount_rate=30, url="https://eeveryday.ssg.com", category="간편식", badge="근거리배송"),
    Promotion(id="everyday_2", platform="everyday", platform_name="이마트 에브리데이", title="이마트 에브리데이 신선 샐러드 250g", original_price=3900, sale_price=2730, discount_rate=30, url="https://eeveryday.ssg.com", category="샐러드"),
    Promotion(id="everyday_3", platform="everyday", platform_name="이마트 에브리데이", title="매일유업 바나나맛 우유 200ml×6개", original_price=5400, sale_price=3780, discount_rate=30, url="https://eeveryday.ssg.com", category="유제품"),
    Promotion(id="everyday_4", platform="everyday", platform_name="이마트 에브리데이", title="CJ 고메소시지 380g (1+1)", original_price=5900, sale_price=2950, discount_rate=50, url="https://eeveryday.ssg.com", category="육가공", badge="1+1"),
    Promotion(id="everyday_5", platform="everyday", platform_name="이마트 에브리데이", title="노브랜드 김치 500g (국내산 배추)", original_price=5900, sale_price=4130, discount_rate=30, url="https://eeveryday.ssg.com", category="김치"),
]

async def fetch() -> List[Promotion]:
    return SAMPLE
