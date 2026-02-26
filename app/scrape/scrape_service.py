"""Wildberries catalog and product detail scraping service."""

import logging
from typing import Any, Dict, List

from app.core.client import HttpClient
from app.core.config import settings
from app.core.utils import build_image_urls, build_search_url, throttle

logger = logging.getLogger(settings.PROJECT_NAME)


class WildberriesScraper:  # pylint: disable=missing-class-docstring
    def __init__(self, client: HttpClient) -> None:
        self._client = client

    async def fetch_search_page(
        self, query: str, page: int = 1
    ) -> List[Dict[str, Any]]:
        url = build_search_url(settings.WB_SEARCH_URL, query, page)
        logger.info("Fetching search page %d for query: %r", page, query)
        data = await self._client.get_json(url)
        if not data:
            logger.warning("Empty response on page %d, stopping pagination", page)
            return []
        products = data.get("products") or []
        logger.info("Page %d returned %d products", page, len(products))
        return products

    async def fetch_all_products(self, query: str) -> List[Dict[str, Any]]:
        all_products: List[Dict[str, Any]] = []
        for page in range(1, settings.MAX_PAGES + 1):
            products = await self.fetch_search_page(query, page)
            if not products:
                break
            all_products.extend(products)
            await throttle(settings.REQUEST_DELAY)
        logger.info("Total products collected: %d", len(all_products))
        return all_products

    def attach_image_urls(self, products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        for product in products:
            article = product.get("id")
            pics = product.get("pics", 1)
            product["_image_urls"] = build_image_urls(
                article, pics, settings.WB_IMAGES_URL
            )
            logger.debug("Article %s: built %d image URLs", article, pics)
        return products
