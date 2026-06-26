"""오프라인 마트 전단지 공통 수집 로직.

각 마트의 '이번주 전단' 공식 뷰어 URL은 마트가 매주 자동으로 최신 전단으로
교체한다. 따라서 그 URL의 페이지에서 전단 이미지를 추출하면 항상 '지금 이번주'
전단만 나온다. 서버(Render)에서 직접 받아 이미지 URL을 추출하고, 차단되거나
이미지를 못 찾으면 공식 뷰어로 바로 가는 카드 1장으로 폴백한다.
"""
import re
import httpx
from typing import List, Optional
from models import Promotion

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Linux; Android 13; SM-S918N) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/121.0.0.0 Mobile Safari/537.36"
    ),
    "Accept-Language": "ko-KR,ko;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
}

# 콘텐츠 이미지가 아닌 아이콘/로고/버튼류를 걸러내는 키워드
SKIP_IMG_HINTS = (
    "logo", "icon", "btn", "button", "sprite", "blank", "spacer",
    "bg_", "_bg", "common", "header", "footer", "arrow", "loading",
    ".svg", ".gif", "facebook", "kakao", "qr",
)

IMG_URL_RE = re.compile(
    r"""https?://[^\s"'()<>]+?\.(?:jpg|jpeg|png|webp)(?:\?[^\s"'()<>]*)?""",
    re.IGNORECASE,
)


def _is_content_image(url: str) -> bool:
    low = url.lower()
    if any(h in low for h in SKIP_IMG_HINTS):
        return False
    return True


def _extract_images(html: str, allow_hosts: tuple) -> List[str]:
    """페이지 HTML에서 전단 이미지로 보이는 절대 URL을 추출 (클래스명에 의존하지 않음)."""
    found = []
    seen = set()
    for m in IMG_URL_RE.finditer(html):
        url = m.group(0)
        if url in seen:
            continue
        if allow_hosts and not any(h in url for h in allow_hosts):
            continue
        if not _is_content_image(url):
            continue
        seen.add(url)
        found.append(url)
    return found


async def fetch_flyer(
    platform: str,
    platform_name: str,
    page_url: str,
    official_view_url: str,
    allow_hosts: tuple,
    cover_image: Optional[str] = None,
) -> List[Promotion]:
    """공식 '이번주 전단' 페이지에서 이미지 추출. 실패 시 공식 뷰어 링크 카드로 폴백."""
    images: List[str] = []
    try:
        async with httpx.AsyncClient(timeout=12.0, follow_redirects=True) as c:
            r = await c.get(page_url, headers=HEADERS)
            if r.status_code == 200:
                images = _extract_images(r.text, allow_hosts)
    except Exception:
        images = []

    results: List[Promotion] = []
    for i, img in enumerate(images[:15]):
        results.append(Promotion(
            id=f"{platform}_{i}",
            platform=platform,
            platform_name=platform_name,
            title=f"{platform_name} · 이번주 전단행사",
            image_url=img,
            url=official_view_url,
            category="전단지",
        ))

    # 폴백: 이미지를 못 가져왔으면 공식 뷰어로 바로 가는 카드 1장
    if not results:
        results.append(Promotion(
            id=f"{platform}_official",
            platform=platform,
            platform_name=platform_name,
            title=f"{platform_name} 이번주 전단행사 전체보기 (오늘 기준 최신)",
            image_url=cover_image,
            url=official_view_url,
            category="전단지",
        ))

    return results
