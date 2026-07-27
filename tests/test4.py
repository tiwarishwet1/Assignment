from src.browserstack.driver_factory import DriverFactory
from src.scraper.el_pais_scraper import ElPaisScraper
from src.translator.translator_service import DeepTranslatorService
from src.analyzer.text_analyzer import WordFrequencyAnalyzer
from src.services.article_pipeline import ArticlePipeline
from src.utils.report_generator import ReportGenerator
from src.utils.logger import logger

def verify_pipeline():
    print("=" * 60)
    print("🔍 VERIFYING PHASE 4: LOCAL END-TO-END PIPELINE & REPORTING")
    print("=" * 60)

    driver = DriverFactory.create_local_driver("chrome")
    try:
        # 1. Instantiate concrete implementations
        scraper = ElPaisScraper(driver)
        translator = DeepTranslatorService()
        analyzer = WordFrequencyAnalyzer()

        # 2. Inject dependencies into Pipeline Orchestrator
        pipeline = ArticlePipeline(scraper, translator, analyzer)
        articles, repeated_words = pipeline.execute(section_name="opinion", limit=5)

        # 3. Generate Reports
        ReportGenerator.generate_json_report(articles, repeated_words, session_name="Local_Chrome")
        summary = ReportGenerator.generate_text_summary(articles, repeated_words)

        print("\n" + summary)
        print("🎉 PHASE 4 VERIFICATION PASSED PERFECTLY!")
    except Exception as e:
        print(f"\n❌ Phase 4 Pipeline Execution Failed: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    verify_pipeline()