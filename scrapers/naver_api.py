import os
import re
import httpx
from typing import List, Optional
from urllib.parse import urlparse, parse_qs, unquote
from models import Promotion

NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID", "")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET", "")

FOOD_CATEGORIES = {"식품", "음식료/담배", "식품/생필품"}

PLATFORM_RULES = [
    (["쿠팡"],           "coupang",  "쿠팡"),
    (["마켓컬리", "컬리"], "kurly",    "컬리"),
    (["이마트에브리데이"],  "everyday", "이마트에브리데이"),
    (["트레이더스"],       "traders",  "트레이더스"),
    (["이마트"],          "emart",    "이마트"),
    (["롯데온"],          "lotteon",  "롯데ON"),
    (["롯데마트"],         "lotte",    "롯데마트"),
    (["홈플러스"],         "homeplus", "홈플러스"),
    (["코스트코"],         "costco",   "코스트코"),
    (["SSG", "신세계"],   "ssg",      "SSG"),
    (["11번가"],          "eleven",   "11번가"),
    (["토스"],            "toss",     "토스쇼핑"),
]

def detect_platform(mall_name: str):
    for keywords, platform, name in PLATFORM_RULES:
        if any(kw in mall_name for kw in keywords):
            return platform, name
    return "naver", "네이버쇼핑"

def clean_title(title: str) -> str:
    return re.sub(r"</?b>", "", title).strip()

def is_available() -> bool:
    return bool(NAVER_CLIENT_ID and NAVER_CLIENT_SECRET)

def is_food_item(item: dict) -> bool:
    cat1 = item.get("category1", "")
    if cat1 in FOOD_CATEGORIES:
        return True
    # category1이 비어있으면 category2로 판단
    if not cat1:
        cat2 = item.get("category2", "")
        food_keywords = ["과일", "채소", "정육", "수산", "유제품", "달걀", "계란", "라면", "즉석", "음료", "커피", "과자", "스낵", "김치", "반찬", "밥", "면"]
        return any(kw in cat2 for kw in food_keywords)
    return False

async def search(query: str, display: int = 20) -> List[dict]:
    if not is_available():
        return []
    try:
        async with httpx.AsyncClient(timeout=8.0) as c:
            r = await c.get(
                "https://openapi.naver.com/v1/search/shop.json",
                params={"query": query, "display": display, "sort": "sim"},
                headers={
                    "X-Naver-Client-Id": NAVER_CLIENT_ID,
                    "X-Naver-Client-Secret": NAVER_CLIENT_SECRET,
                },
            )
            if r.status_code == 200:
                return r.json().get("items", [])
    except Exception:
        pass
    return []

def _price_discount_rate(item: dict) -> int:
    """lprice/hprice 격차로 정렬용 할인율 추정 (0이면 단일가)."""
    lp = int(item.get("lprice", 0) or 0)
    hp = int(item.get("hprice", 0) or 0)
    return int((hp - lp) / hp * 100) if hp > lp > 0 else 0


def _resolve_link(raw_link: str, product_id: str) -> Optional[str]:
    """Return the best accessible URL for a product.

    Naver Shopping API wraps all links in link.shopping.naver.com tracking URLs
    that force login. We try to extract the real destination URL from query params,
    and fall back to the catalog page which is publicly accessible.
    """
    if not raw_link or "link.shopping.naver.com" in raw_link:
        if raw_link:
            # Try to extract actual destination from tracking URL query params
            try:
                parsed = urlparse(raw_link)
                params = parse_qs(parsed.query)
                for key in ("url", "destination", "dest", "target"):
                    if key in params:
                        dest = unquote(params[key][0])
                        if dest.startswith("http"):
                            return dest
            except Exception:
                pass
        # Fall back to Naver catalog page (publicly accessible, no login)
        if product_id:
            return f"https://search.shopping.naver.com/catalog/{product_id}"
        return None
    return raw_link

def to_promotion(item: dict, idx: int, force_platform: Optional[str] = None, force_name: Optional[str] = None) -> Optional[Promotion]:
    title = clean_title(item.get("title", ""))
    image = item.get("image", "")
    lprice = int(item.get("lprice", 0) or 0)
    hprice = int(item.get("hprice", 0) or 0) or lprice
    mall = item.get("mallName", "")
    category = item.get("category4") or item.get("category3") or item.get("category2") or ""
    product_id = item.get("productId", "")

    if not title or not image:
        return None

    raw_link = item.get("link", "")
    link = _resolve_link(raw_link, product_id)
    if not link:
        return None

    platform, platform_name = (force_platform, force_name) if force_platform else detect_platform(mall)
    discount_rate = int((hprice - lprice) / hprice * 100) if hprice > lprice else 0

    return Promotion(
        id=f"{platform}_nv_{idx}",
        platform=platform,
        platform_name=platform_name,
        title=title,
        image_url=image or None,
        original_price=hprice if hprice != lprice else None,
        sale_price=lprice or None,
        discount_rate=discount_rate or None,
        url=link,
        category=category or None,
        badge=None,
    )

