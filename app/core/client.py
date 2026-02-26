"""Async HTTP client lifecycle management via aiohttp."""

import logging
from typing import Any, Optional

import aiohttp

from app.core.config import settings

logger = logging.getLogger(settings.PROJECT_NAME)

HEADERS = {
    "User-Agent": settings.USER_AGENT,
    "Accept": settings.ACCEPT,
    "Accept-Language": settings.ACCEPT_LANGUAGE,
    "Origin": settings.ORIGIN,
    "Cookie": settings.COOKIE,
    "sec-ch-ua": "'Opera GX';v='127', 'Chromium';v='143', 'Not A(Brand';v='24'",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Windows",
}


class HttpClient:  # pylint: disable=missing-class-docstring
    def __init__(self) -> None:
        self._session: Optional[aiohttp.ClientSession] = None

    async def open(self) -> None:
        connector = aiohttp.TCPConnector(ssl=False, limit=3)
        timeout = aiohttp.ClientTimeout(total=30)
        self._session = aiohttp.ClientSession(
            headers=HEADERS,
            connector=connector,
            timeout=timeout,
        )

    async def close(self) -> None:
        if self._session:
            await self._session.close()
            self._session = None

    async def get_json(self, url: str, **kwargs: Any) -> Optional[dict]:
        if not self._session:
            raise RuntimeError("Client is not open. Call open() first.")
        logger.debug("GET %s", url)
        try:
            async with self._session.get(url, **kwargs) as resp:
                logger.debug("Response %s from %s", resp.status, url)
                if resp.status == 200:
                    return await resp.json(content_type=None)
                logger.warning("Non-200 status %s for URL: %s", resp.status, url)
                return None
        except aiohttp.ClientError as exc:
            logger.error("Request failed for %s: %s", url, exc)
            return None

    async def __aenter__(self) -> "HttpClient":
        await self.open()
        return self

    async def __aexit__(self, *_: Any) -> None:
        await self.close()
