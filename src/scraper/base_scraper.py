from abc import ABC, abstractmethod
from typing import List
from selenium.webdriver.remote.webdriver import WebDriver
from src.models.article import Article


class BaseScraper(ABC):

    def __init__(self, driver: WebDriver):
        self.driver = driver

    @abstractmethod
    def scrape_section(
        self, section_name: str = "opinion", limit: int = 5
    ) -> List[Article]:
        """Scrapes section and returns a list of Article models."""
        pass
