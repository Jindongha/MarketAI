import os
import re
import httpx
from typing import List, Optional
from models import Promotion

NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID", "")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET", "")

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

async def search(query: str, display: int = 20) -> List[dict]:
    if not is_available():
        return []
    try:
        async with httpx.AsyncClient(timeout=8.0) as c:
            r = await c.get(
                "https://openapi.naver.com/v1/search/shop.json",
                params={"query": query, "display": display, "sort": "asc"},
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

def to_promotion(item: dict, idx: int, force_platform: Optional[str] = None, force_name: Optional[str] = None) -> Optional[Promotion]:
    title = clean_title(item.get("title", ""))
    image = item.get("image", "")
    lprice = int(item.get("lprice", 0) or 0)
    hprice = int(item.get("hprice", 0) or 0) or lprice
    mall = item.get("mallName", "")
    category = item.get("category4") or item.get("category3") or item.get("category2") or ""
    product_id = item.get("productId", "")

    if not title:
        return None

    # Naver catalog URL is always accessible (no login, no app required)
    if product_id:
        link = f"https://search.shopping.naver.com/catalog/{product_id}"
    else:
        seller_link = item.get("link", "")
        if seller_link and seller_link.startswith("http"):
            link = seller_link
        else:
            # fallback: Naver Shopping search by title
            import urllib.parse
            link = f"https://search.shopping.naver.com/search/all?query={urllib.parse.quote(title)}"

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
        badge="네이버쇼핑" if platform == "naver" else None,
    )
