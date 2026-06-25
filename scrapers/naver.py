from typing import List
from models import Promotion
from scrapers.images import get_image

SAMPLE: List[Promotion] = [
    Promotion(id="naver_1", platform="naver", platform_name="네이버쇼핑", title="경상북도 사과 5kg 선물용 (부사)", original_price=39000, sale_price=27300, discount_rate=30, url="https://search.shopping.naver.com/search/all?query=사과5kg", category="과일", badge="N페이", image_url=get_image("과일","")),
    Promotion(id="naver_2", platform="naver", platform_name="네이버쇼핑", title="완도 활전복 1kg (중·소혼합)", original_price=48000, sale_price=33600, discount_rate=30, url="https://search.shopping.naver.com/search/all?query=활전복", category="수산물", image_url=get_image("수산물","")),
    Promotion(id="naver_3", platform="naver", platform_name="네이버쇼핑", title="친환경 유정란 30구 (무항생제 인증)", original_price=14000, sale_price=9800, discount_rate=30, url="https://search.shopping.naver.com/search/all?query=유정란30구", category="달걀", badge="플러스회원", image_url=get_image("달걀","")),
    Promotion(id="naver_4", platform="naver", platform_name="네이버쇼핑", title="국내산 표고버섯 선물세트 1.5kg", original_price=55000, sale_price=38500, discount_rate=30, url="https://search.shopping.naver.com/search/all?query=표고버섯선물세트", category="채소", image_url=get_image("채소","")),
    Promotion(id="naver_5", platform="naver", platform_name="네이버쇼핑", title="전라도 반찬 모음 10종 세트", original_price=35000, sale_price=24500, discount_rate=30, url="https://search.shopping.naver.com/search/all?query=반찬모음세트", category="간편식", badge="BEST", image_url=get_image("김치","")),
]

async def fetch() -> List[Promotion]:
    return SAMPLE
