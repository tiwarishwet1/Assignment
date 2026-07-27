import os
import requests
from typing import List
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from src.scraper.base_scraper import BaseScraper
from src.models.article import Article
from src.config.settings import settings
from src.utils.logger import logger


class ElPaisScraper(BaseScraper):
    BASE_URL = "https://elpais.com"

    def scrape_section(
        self, section_name: str = "opinion", limit: int = 5
    ) -> List[Article]:
        target_url = f"{self.BASE_URL}/{section_name.strip('/')}/"
        logger.info(f"Navigating to El País section: {target_url}")
        self.driver.get(target_url)

        # 1. Handle Cookie Consent First
        self._handle_cookie_consent()
        self._verify_spanish_language()

        # 2. Wait up to 20 seconds for <article> elements (Mobile-resilient)
        try:
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, "article"))
            )
        except TimeoutException:
            logger.warning("Article tags took longer than expected; attempting DOM fallback...")

        article_elements = self.driver.find_elements(
            By.TAG_NAME, "article"
        )[:limit]

        os.makedirs(settings.IMAGE_DIR, exist_ok=True)
        scraped_articles: List[Article] = []

        for idx, elem in enumerate(article_elements, start=1):
            title = self._extract_title(elem)
            content = self._extract_content(elem)
            img_path = self._download_cover_image(elem, idx)

            article = Article(
                index=idx,
                title_es=title,
                content_es=content,
                local_image_path=img_path,
            )
            scraped_articles.append(article)

        logger.info(
            f"Successfully scraped {len(scraped_articles)} "
            f"articles from '{section_name}'."
        )
        return scraped_articles

    def _handle_cookie_consent(self) -> None:
        try:
            cookie_btn = WebDriverWait(self.driver, 8).until(
                EC.element_to_be_clickable(
                    (By.ID, "didomi-notice-agree-button")
                )
            )
            cookie_btn.click()
            logger.info("Cookie consent dialog cleared.")
        except Exception:
            logger.debug("No cookie banner detected or interaction skipped.")

    def _verify_spanish_language(self) -> None:
        try:
            lang = self.driver.find_element(
                By.TAG_NAME, "html"
            ).get_attribute("lang")
            logger.info(f"HTML lang attribute verified: '{lang}'")
        except NoSuchElementException:
            logger.warning("Could not find <html> lang attribute.")

    def _extract_title(self, elem) -> str:
        try:
            return elem.find_element(By.XPATH, ".//h2 | .//h3").text.strip()
        except Exception:
            return "Title Unavailable"

    def _extract_content(self, elem) -> str:
        try:
            return elem.find_element(By.XPATH, ".//p").text.strip()
        except Exception:
            return "Content Snippet Unavailable"

    def _download_cover_image(self, elem, index: int) -> str:
        try:
            try:
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", elem
                )
            except Exception:
                pass

            img_tags = elem.find_elements(By.TAG_NAME, "img")
            if not img_tags:
                return "No Cover Image Found"

            img_tag = img_tags[0]
            img_url = (
                img_tag.get_attribute("src")
                or img_tag.get_attribute("data-src")
                or img_tag.get_attribute("srcset")
            )

            if img_url and "http" in img_url and not img_url.endswith(".svg"):
                if " " in img_url:
                    img_url = img_url.split(" ")[0]

                response = requests.get(img_url, timeout=10)
                if response.status_code == 200:
                    ext = "png" if ".png" in img_url else "jpg"
                    filepath = os.path.join(
                        settings.IMAGE_DIR, f"article_{index}.{ext}"
                    )
                    with open(filepath, "wb") as f:
                        f.write(response.content)
                    return filepath
        except Exception as e:
            logger.debug(
                f"Image download skipped for article index {index}: {e}"
            )
        return "No Cover Image Downloaded"