from bs4 import BeautifulSoup
from contextlib import contextmanager
from datetime import datetime, timedelta
from loguru import logger
from playwright.sync_api._generated import Playwright, Browser
from typing import Any, Dict, List, Generator

from database import Database
from models import Article


class ArticleFetcher:
    _page_url_template: str = 'https://laravel-news.com/blog?tag=news&page={}'
    _page_number: int = 1

    def __init__(self, playwright: Playwright, database: Database) -> None:
        """
        Constructor
        """
        self._get_session = database.get_session
        self._p = playwright
        logger.info("ArticleFetcher initialized")

    @property
    def next_page_url(self) -> str:
        """
        Every call will return a next page url
        :return: url of the next page
        """
        page_url = self._page_url_template.format(self._page_number)
        self._page_number += 1
        return page_url

    @contextmanager
    def get_browser(self) -> Generator[Browser, None, None]:
        """
        Context manager for closing browser
        :return: browser instance
        """
        browser = self._p.chromium.launch(headless=False)
        try:
            yield browser
        except Exception as e:
            logger.error(f"Error during browser operation: {e}")
        finally:
            browser.close()

    def fetch_articles(self) -> None:
        """
        Enrtypoint
        :return: nothing
        """
        logger.info("Starting to fetch articles")

        with self.get_browser() as browser:
            page = browser.new_page()
            while True:
                page_url = self.next_page_url
                logger.info(f"Fetching page {page_url}")
                
                page.goto(page_url)
                html_content = page.content()
                articles = self.parse_articles_from_html(html_content)

                if not articles:
                    logger.info(f"No more articles found on page {self._page_number}")
                    break

                for article in articles:
                    if self.should_stop_processing(article['url']):
                        logger.info(f"Skipping article due to existing record in database: {article['url']}")
                        continue

                    details = self.fetch_article_details(article['url'])

                    if not details:
                        logger.warning(f"Can`t fetch article details: {article['url']}")
                        break

                    if self.is_older_than_four_months(details['publication_date']):
                        logger.info(f"Stopping processing due to publication date: {article['url']}")
                        break

                    self.save_article({**article, **details})
                else: # if no break cases happened
                    continue 
                break # break main loop due to existing article or publication date

    def parse_articles_from_html(self, html: str) -> List[Dict]:
        """
        Find all articles on page
        :return: list of articles data from feed page
        """
        soup = BeautifulSoup(html, 'html.parser')
        article_nodes = soup.select('section.py-20 div.group.relative')
        articles = []

        for node in article_nodes:
            title = node.select_one('h3')
            url = node.select_one('a')
            if title and url:
                if url['href'] == "/advertising":
                    continue # Skipping advertisments
                articles.append({'title': title.get_text(), 'url': url['href']})

        return articles

    def fetch_article_details(self, url: str) -> Dict[str, Any] | None:
        """
        Find additional information about article
        :return: additional data by the article
        """
        with self.get_browser() as browser:
            page = browser.new_page()
            page.goto(url)
            html_content = page.content()
            soup = BeautifulSoup(html_content, 'html.parser')

            publication_date_node = soup.select_one('time[itemprop="dateModified"]')
            author_node = soup.select_one('a[rel="author"]')
            if not publication_date_node or not author_node:
                logger.error(f"Missing required nodes for URL: {url}")
                return None
            publication_date = publication_date_node['datetime']
            author = author_node.get_text()

            tags_node = soup.find('div', class_="flex flex-wrap items-center gap-x-2 gap-y-2")
            tag_links =  [
                "https://laravel-news.com/"+a['href'] for a in tags_node.find_all('a', href=True)
            ]

            return {
                'publication_date': self.parse_date(publication_date),
                'author': author,
                'tags': ", ".join(tag_links)
            }

    def parse_date(self, date_str: str) -> datetime | None:
        """
        Convert date from string to datetime object for future calculations
        :return: datetime object if date_str is correct
        """
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S')
            return date_obj
        except Exception as e:
            logger.error(f"Error parsing date: {date_str} -> {e}")
            return None

    def is_older_than_four_months(self, article_date: datetime) -> bool:
        """
        Check article`s date object
        """
        four_months_ago = datetime.now() - timedelta(days=4*30)
        return article_date < four_months_ago

    def should_stop_processing(self, url: str) -> bool:
        """
        Check if article already exists in database
        """
        with self._get_session() as session:
            existing_article = session.query(Article).filter(Article.url == url).first()
            return existing_article is not None
        return False

    def save_article(self, data: dict) -> None:
        """
        Add record to database
        """
        with self._get_session() as session:
            article = Article(
                title=data['title'],
                url=data['url'],
                publication_date=data['publication_date'],
                author=data['author'],
                tags=data['tags']
            )
            session.add(article)
            logger.info(f"Article saved: {data['title']}")