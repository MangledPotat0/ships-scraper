# -*- coding: utf-8 -*-
"""
/run.py
Process for scraping web sources to populate ships db.
"""

# Built-in module import
import time
from typing import List

# Local module imoprt
import app.scrape.imo as imo
import app.scrape.scraper as sc
from app.scrape.sources import Source

def run(sources: List[Sources]):
    """
    Runs the polling loop.

    Args:
        sources (List[Sources]): List of source enums to process.
    """

    scrapers = [sc.Scraper(source) for source in sources]
    # For now just use a single source
    scraper = scraper[0]
    # Fetch from server with noisy period to make it look less sus
    interval = 120 + np.random.random(-6, high=6)
    next_time = time.monotonic()
    while True:
        dataframe = scraper.scrape(imo)
        next_time += interval
        time.sleep(max(0,next_time - time.monotonic()))
    return

if __name__ == "__main__":
    sources = [Source.VESSELFINDER]
    run(sources)
