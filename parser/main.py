from playwright.sync_api import sync_playwright

from constants import DB_URI
from database import Database
from models import Base
from fetcher import ArticleFetcher
from logger import setup_logging

if __name__ == "__main__":
    setup_logging()
    database = Database(DB_URI)
    Base.metadata.create_all(database.engine)

    with sync_playwright() as playwright:
        fetcher = ArticleFetcher(playwright, database)
        fetcher.fetch_articles()
