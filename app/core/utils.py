"""Helper utilities for URL building and image basket resolution."""

import asyncio
from typing import List


def build_search_url(base_url: str, query: str, page: int = 1) -> str:
    url = base_url.format(query=query)
    if page > 1:
        url += f"&page={page}"
    return url


def resolve_basket(vol: int) -> int:
    thresholds = [
        (143, 1),
        (287, 2),
        (431, 3),
        (719, 4),
        (1007, 5),
        (1061, 6),
        (1115, 7),
        (1169, 8),
        (1313, 9),
        (1601, 10),
        (1655, 11),
        (1919, 12),
        (2045, 13),
        (2189, 14),
        (2405, 15),
        (2621, 16),
        (2837, 17),
        (3053, 18),
        (3269, 19),
        (3485, 20),
        (3701, 21),
        (3917, 22),
        (4133, 23),
        (4349, 24),
        (4565, 25),
        (4904, 26),
        (5244, 27),
        (5584, 28),
        (5923, 29),
        (6263, 30),
        (6602, 31),
        (6942, 32),
        (7281, 33),
        (7480, 34),
        (7760, 35),
        (8300, 36),
        (8639, 37),
        (8979, 38),
        (9318, 39),
        (9658, 40),
    ]
    for threshold, basket in thresholds:
        if vol <= threshold:
            return basket
    return 41


def build_image_urls(article: int, pics: int, url_template: str) -> List[str]:
    vol = article // 100000
    part = article // 1000
    basket = resolve_basket(vol)
    return [
        url_template.format(basket=basket, vol=vol, part=part, article=article, idx=i)
        for i in range(1, pics + 1)
    ]


async def throttle(delay: float) -> None:
    await asyncio.sleep(delay)
