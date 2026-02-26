# <p align="center"> Wildberries Catalog Parser </p>

[![CI](https://github.com/kodokunoaki/WBParser/actions/workflows/pylint.yml/badge.svg)](https://github.com/kodokunoaki/WBParser/actions)

## Overview

A CLI tool that scrapes Wildberries product listings for a given search query фnd exports results into two XLSX files:
- **Full catalog** - all products found for the query
- **Filtered catalog** - products matching rating >= 4.5, price <= 10,000 RUB

## Service Dependencies

| Service | Purpose |
|---|---|
| Wildberries Search API | Paginated search results |
| Wildberries Image CDN | Product image URL resolution |

No external service accounts or API keys required - the parser uses the same public endpoints the website uses.

## Technology Stack

| Layer | Library |
|---|---|
| Async HTTP | aiohttp |
| Configuration | pydantic-settings |
| Data processing | pandas |
| Excel output | openpyxl |
| Runtime | Python 3.11+ |

## Prerequisites

- Python 3.11 or higher
- pip

## Launch Instructions

1. Clone or unzip the project:
   ```bash
   git clone https://github.com/kodokunoaki/WBParser.git
   cd WBParser
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. (Optional) Copy and edit environment config:
   ```bash
   cp .env.example .env
   # edit .env to change query, pagination limits, filter thresholds, etc.
   ```

5. Run the parser:
   ```bash
   python3 -m app.main
   ```

6. Results are saved to the `output/` directory:
   - `output/catalog_full.xlsx` - complete scraped catalog
   - `output/catalog_filtered.xlsx` - filtered selection

## Project Structure

```
wb_parser/
  app/
    core/
      config.py          # pydantic-settings configuration
      client.py          # aiohttp session lifecycle
      utils.py           # URL builders and helpers
    scrape/
      scrape_service.py  # Wildberries API fetching logic
    process/
      process_service.py # Data normalization and filtering
    data/
      save_data.py       # XLSX export with styling
    main.py              # Orchestration entry point
  requirements.txt
  .env.example
  README.md
```

## Scaling Directions

- **API** - add API layer over parser application
- **WB card product information** - add card url processing to get description data for each product
- **Multiple queries** - extend `main.py` to accept CLI arguments via `argparse` and run multiple queries sequentially or concurrently
- **Proxy rotation** - add proxy support to `HttpClient` via `aiohttp` `proxy` parameter to avoid IP bans on large-scale scraping
- **Database storage** - swap `DataSaver` for a SQLAlchemy-based saver targeting PostgreSQL; `process_service.py` output remains unchanged
- **Scheduling** - wrap `main()` in a cron job or APScheduler task for periodic catalog updates
- **Category scraping** - replace the search endpoint with category/filter API endpoints to scrape entire product trees
