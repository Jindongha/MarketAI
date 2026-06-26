import asyncio
import re
import httpx
from bs4 import BeautifulSoup
from typing import List, Optional
from models import Promotion

# 쿠팡은 네이버쇼핑에 더 이상 입점하지 않으므로 쿠팡 직접 크롤링
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Linux; Android 12; SM-G998B) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.4472.124 Mobile Safari/537.36"
    ),
    "Accept-Language": "ko-KR,ko;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Referer": "https://www.coupang.com/",
}

SEARCH_QUERIES = [
    "신선식품 할인",
    "식품 특가",
    "과일 채소 할인",
]


def _parse_price(text: str) -> Optional[int]:
    digits = re.sub(r"[^0-9]", "", text)
    return int(digits) if digits else None


def _extract_from_html(html: str, id_offset: int) -> List[Promotion]:
    soup = BeautifulSoup(html, "lxml")
    results: List[Promotion] = []

    items = (
        soup.select("ul.search-product-list > li.search-product") or
        soup.select("ul#productList > li") or
        soup.select(".search-product") or
        []
    )

    for i, item in enumerate(items):
        if item.select_one(".ad-badge") or "ad" in " ".join(item.get("class", [])):
            continue

        name_el = item.select_one(".name") or item.select_one("h2.name")
        price_el = (
            item.select_one(".price-value") or
            item.select_one("strong.price-value") or
            item.select_one(".price")
        )
        img_el = item.select_one("img.search-product-wrap-img") or item.select_one("img")
        link_el = item.select_one("a.search-product-link") or item.select_one("a[href]")

        if not name_el or not link_el:
            continue

        title = name_el.get_text(strip=True)
        if not title or len(title) < 3:
            continue

        img_src: Optional[str] = None
        if img_el:
            src = img_el.get("src") or img_el.get("data-src") or ""
            if src and not src.startswith("data:"):
                img_src = src if src.startswith("http") else "https:" + src

        href = link_el.get("href", "")
        if href.startswith("/"):
            href = "https://www.coupang.com" + href
        if not href.startswith("http"):
            continue

        sale_price = _parse_price(price_el.get_text(strip=True)) if price_el else None

        orig_el = item.select_one(".base-price") or item.select_one(".original-price")
        original_price = _parse_price(orig_el.get_text(strip=True)) if orig_el else None
        discount_rate: Optional[int] = None
        if original_price and sale_price and original_price > sale_price:
            discount_rate = int((original_price - sale_price) / original_price * 100)

        results.append(Promotion(
            id=f"coupang_{id_offset + i}",
            platform="coupang",
            platform_name="쿠팡",
            title=title,
            image_url=img_src,
            original_price=original_price,
            sale_price=sale_price,
            discount_rate=discount_rate,
            url=href,
        ))

    return results


async def _fetch_url(url: str, id_offset: int) -> List[Promotion]:
    try:
        async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as c:
            r = await c.get(url, headers=HEADERS)
            if r.status_code == 200:
                return _extract_from_html(r.text, id_offset)
    except Exception:
        pass
    return []


async def fetch() -> List[Promotion]:
    urls = [
        f"https://www.coupang.com/np/search?q={q.replace(' ', '+')}&channel=user&sorter=scoreDesc"
        for q in SEARCH_QUERIES
    ]
    results = await asyncio.gather(*[_fetch_url(u, i * 30) for i, u in enumerate(urls)])

    seen_titles: set = set()
    all_items: List[Promotion] = []
    for group in results:
        for item in group:
            if item.title not in seen_titles:
                seen_titles.add(item.title)
                all_items.append(item)

    all_items.sort(key=lambda x: x.discount_rate or 0, reverse=True)
    return all_items[:25]
