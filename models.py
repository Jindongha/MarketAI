from pydantic import BaseModel
from typing import Optional, List


class Promotion(BaseModel):
    id: str
    platform: str
    platform_name: str
    title: str
    image_url: Optional[str] = None
    original_price: Optional[int] = None
    sale_price: Optional[int] = None
    discount_rate: Optional[int] = None
    url: str
    category: Optional[str] = None
    badge: Optional[str] = None


class PromotionsResponse(BaseModel):
    items: List[Promotion]
    total: int


class StoreGroup(BaseModel):
    """전체 보기 화면에서 매장 한 곳의 인기·할인 상품 묶음."""
    platform: str
    platform_name: str
    items: List[Promotion]


class SummaryResponse(BaseModel):
    groups: List[StoreGroup]
    total: int
