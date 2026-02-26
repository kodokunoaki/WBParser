"""Product data transformation and normalization service."""

import logging
from typing import Any, Dict, List, Optional

import pandas as pd

from app.core.config import settings

logger = logging.getLogger(settings.PROJECT_NAME)


def _extract_price(sizes: List[Dict[str, Any]]) -> Optional[float]:
    for size in sizes:
        raw = size.get("price", {}).get("product")
        if raw:
            return round(raw / 100, 2)
    return None


def _extract_sizes(sizes: List[Dict[str, Any]]) -> str:
    names = [s.get("origName") or s.get("name") or "" for s in sizes]
    return ", ".join(filter(None, names))


def _extract_stock(product: Dict[str, Any]) -> int:
    return product.get("totalQuantity", 0)


def _build_row(product: Dict[str, Any]) -> Dict[str, Any]:
    article = product.get("id", "")
    sizes = product.get("sizes", [])
    price = _extract_price(sizes)
    if price is None:
        logger.debug("Article %s: no price found in any size", article)
    return {
        "url": settings.WB_PRODUCT_URL.format(article=article),
        "article": article,
        "name": product.get("name", ""),
        "price": price,
        "images": ", ".join(product.get("_image_urls", [])),
        "seller_name": product.get("supplier", ""),
        "seller_url": settings.WB_SELLER_URL.format(
            seller_id=product.get("supplierId", "")
        ),
        "sizes": _extract_sizes(sizes),
        "stock": _extract_stock(product),
        "rating": product.get("reviewRating") or product.get("nmReviewRating"),
        "reviews_count": product.get("feedbacks", 0),
    }


class ProductProcessor:
    def build_dataframe(self, products: List[Dict[str, Any]]) -> pd.DataFrame:
        logger.info("Building dataframe from %d products", len(products))
        rows = [_build_row(p) for p in products]
        df = pd.DataFrame(rows)
        null_prices = df["price"].isna().sum()
        if null_prices:
            logger.warning("%d products have no price data", null_prices)
        logger.info("Dataframe ready: %d rows, %d columns", len(df), len(df.columns))
        return df

    def filter_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        logger.info(
            "Applying filters: rating>=%.1f, price<=%.0f",
            settings.FILTER_MIN_RATING,
            settings.FILTER_MAX_PRICE,
        )
        before = len(df)
        mask = (df["rating"] >= settings.FILTER_MIN_RATING) & (
            df["price"] <= settings.FILTER_MAX_PRICE
        )
        df_filtered = df[mask].reset_index(drop=True)
        logger.info(
            "Filter result: %d -> %d rows (dropped %d)",
            before,
            len(df_filtered),
            before - len(df_filtered),
        )
        return df_filtered
