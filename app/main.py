"""Entry point: orchestrates scraping, processing, and saving catalog data."""

import asyncio
import logging

from app.core.client import HttpClient
from app.core.config import settings
from app.core.logging import setup_logger
from app.data.save_data import DataSaver
from app.process.process_service import ProductProcessor
from app.scrape.scrape_service import WildberriesScraper

logger = logging.getLogger(settings.PROJECT_NAME)


async def main() -> None:
    query = settings.DEFAULT_QUERY
    logger.info("Starting catalog scrape for query: %s", query)

    async with HttpClient() as client:
        scraper = WildberriesScraper(client)
        processor = ProductProcessor()
        saver = DataSaver()

        logger.info("Fetching search results...")
        products = await scraper.fetch_all_products(query)
        logger.info("Found %d products in search results", len(products))
        if not products:
            logger.warning("No products found. Exiting.")
            return

        products_with_images = scraper.attach_image_urls(products)

        df_full = processor.build_dataframe(products_with_images)
        logger.info("Built full dataframe with %d rows", len(df_full))
        full_path = saver.save_full_catalog(df_full)
        logger.info("Full catalog saved: %s", full_path)

        df_filtered = processor.filter_dataframe(df_full)
        logger.info(
            "Filtered catalog: %d rows (rating>=%.1f, price<=%.0f)",
            len(df_filtered),
            settings.FILTER_MIN_RATING,
            settings.FILTER_MAX_PRICE,
        )
        filtered_path = saver.save_filtered_catalog(df_filtered)
        logger.info("Filtered catalog saved: %s", filtered_path)


if __name__ == "__main__":
    try:
        setup_logger(settings.PROJECT_NAME, f"{settings.PROJECT_NAME}.log")
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server stopped by user.")
