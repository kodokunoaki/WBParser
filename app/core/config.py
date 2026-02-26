"""Application configuration via pydantic-settings."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "WBParser"

    WB_SEARCH_URL: str
    WB_PRODUCT_URL: str = "https://www.wildberries.ru/catalog/{article}/detail.aspx"
    WB_SELLER_URL: str = "https://www.wildberries.ru/seller/{seller_id}"
    WB_IMAGES_URL: str = (
        "https://basket-{basket:02d}.wbbasket.ru/vol{vol}"
        "/part{part}/{article}/images/big/{idx}.webp"
    )

    DEFAULT_QUERY: str
    MAX_PAGES: int = 1
    REQUEST_DELAY: float = 3.5

    OUTPUT_DIR: str = "output"
    FULL_CATALOG_FILENAME: str = "catalog_full.xlsx"
    FILTERED_CATALOG_FILENAME: str = "catalog_filtered.xlsx"

    FILTER_MIN_RATING: float = 4.5
    FILTER_MAX_PRICE: float = 10000.0

    ACCEPT: str
    ACCEPT_LANGUAGE: str
    USER_AGENT: str
    COOKIE: str
    ORIGIN: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
