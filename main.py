import sys
from src.browserstack.driver_factory import DriverFactory
from src.scraper.el_pais_scraper import ElPaisScraper
from src.translator.translator_service import DeepTranslatorService
from src.analyzer.text_analyzer import WordFrequencyAnalyzer
from src.services.article_pipeline import ArticlePipeline
from src.utils.report_generator import ReportGenerator
from src.config.settings import settings
from src.utils.logger import logger


def run():
    logger.info("🚀 Launching El País Scraping Pipeline...")
    driver = None
    try:
        # 1. Driver Factory (Managed by SDK or Local Selenium)
        driver = DriverFactory.create_driver()

        # 2. Inject Concrete Services into Pipeline
        scraper = ElPaisScraper(driver)
        translator = DeepTranslatorService()
        analyzer = WordFrequencyAnalyzer()
        pipeline = ArticlePipeline(scraper, translator, analyzer)

        # 3. Execute Scrape -> Translate -> Analyze Pipeline
        articles, repeated_words = pipeline.execute(
            section_name=settings.TARGET_SECTION,
            limit=settings.SCRAPE_LIMIT
        )

        # 4. Generate Reports
        ReportGenerator.generate_json_report(
            articles, repeated_words, session_name="BrowserStack_SDK_Run"
        )
        ReportGenerator.generate_text_summary(articles, repeated_words)

        logger.info("✅ Execution completed successfully!")

    except Exception as e:
        logger.error(f"❌ Pipeline Execution Failed: {e}")
        sys.exit(1)
    finally:
        if driver:
            driver.quit()


if __name__ == "__main__":
    run()