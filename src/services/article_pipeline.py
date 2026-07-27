from typing import List, Dict, Tuple

from src.scraper.base_scraper import BaseScraper
from src.translator.base_translator import BaseTranslator
from src.analyzer.base_analyzer import BaseAnalyzer
from src.models.article import Article
from src.utils.logger import logger


class ArticlePipeline:

    def __init__(
        self,
        scraper: BaseScraper,
        translator: BaseTranslator,
        analyzer: BaseAnalyzer,
    ):
        self.scraper = scraper
        self.translator = translator
        self.analyzer = analyzer

    def execute(
        self, section_name: str = "opinion", limit: int = 5
    ) -> Tuple[List[Article], Dict[str, int]]:
        logger.info(
            f"--- Launching Execution Pipeline [{section_name}] ---"
        )

        articles = self.scraper.scrape_section(
            section_name=section_name, limit=limit
        )

        translated_headers = []
        for article in articles:
            article.title_en = self.translator.translate_text(article.title_es)
            translated_headers.append(article.title_en)

        repeated_words = self.analyzer.analyze_repeated_words(
            translated_headers, threshold=2
        )

        logger.info("--- Pipeline Execution Complete ---")
        return articles, repeated_words
