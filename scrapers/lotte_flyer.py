import os
import re
import httpx
from datetime import datetime
from typing import List
from models import Promotion

NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID", "")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET", "")


async def _search_images(query: str, display: int = 20) -> List[dict]:
    if not NAVER_CLIENT_ID:
        return []
    try:
        async with httpx.AsyncClient(timeout=8.0) as c:
            r = await c.get(
                "https://openapi.naver.com/v1/search/image.json",
                params={"query": query, "display": display, "sort": "date", "filter": "large"},
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


def _clean(text: str) -> str:
    return re.sub(r"</?b>", "", text).strip()


async def fetch() -> List[Promotion]:
    now = datetime.now()
    query = f"롯데마트 전단지 {now.year}년 {now.month}월 이번주 행사 할인"
    items = await _search_images(query, display=20)

    results: List[Promotion] = []
    seen_links: set = set()

    for i, it in enumerate(items):
        thumb = it.get("thumbnail", "")
        link = it.get("link", "") or it.get("originallink", "")
        title = _clean(it.get("title", "롯데마트 전단지"))

        if not thumb or not link or link in seen_links:
            continue

        combined = (title + link).lower()
        if not any(kw in combined for kw in ["롯데", "lotte", "전단", "행사", "할인"]):
            continue

        if int(it.get("sizewidth", 300)) < 200:
            continue

        seen_links.add(link)
        results.append(Promotion(
            id=f"lotte_flyer_{i}",
            platform="lotte_flyer",
            platform_name="롯데마트 전단",
            title=title or "롯데마트 이번주 전단 행사",
            image_url=thumb,
            url=link,
            category="전단지",
        ))

    return results[:12]
