import argparse
import concurrent.futures
from typing import Dict, Any

from src.config.settings import settings
from src.browserstack.capabilities import get_browserstack_capabilities
from src.browserstack.driver_factory import DriverFactory
from src.scraper.el_pais_scraper import ElPaisScraper
from src.translator.translator_service import DeepTranslatorService
from src.analyzer.text_analyzer import WordFrequencyAnalyzer
from src.services.article_pipeline import ArticlePipeline
from src.utils.report_generator import ReportGenerator
from src.utils.logger import logger

def execute_pipeline_on_capability(capability: Dict[str, Any]) -> dict:
    """
    Worker function executed inside ThreadPoolExecutor.
    Instantiates Remote WebDriver on BrowserStack, runs pipeline, and marks status.
    """
    session_name = capability.get("bstack:options", {}).get("sessionName", "BrowserStack Thread")
    logger.info(f"🚀 [START] Launching Cloud Execution: '{session_name}'")

    driver = None
    try:
        # 1. Connect Remote Driver to BrowserStack Grid
        driver = DriverFactory.create_remote_driver(capability)

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

        # 4. Mark Session Status PASSED on BrowserStack Dashboard
        driver.execute_script(
            'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed", "reason": "Pipeline completed successfully!"}}'
        )
        logger.info(f"✅ [SUCCESS] Session Passed: '{session_name}'")

        return {
            "session_name": session_name,
            "status": "passed",
            "articles": articles,
            "repeated_words": repeated_words
        }

    except Exception as e:
        logger.error(f"❌ [FAILURE] Session Failed '{session_name}': {e}")
        if driver:
            try:
                driver.execute_script(
                    f'browserstack_executor: {{"action": "setSessionStatus", "arguments": {{"status":"failed", "reason": "{str(e)[:100]}"}}}}'
                )
            except Exception:
                pass
        return {
            "session_name": session_name,
            "status": "failed",
            "error": str(e)
        }
    finally:
        if driver:
            driver.quit()


def run_local_mode():
    """Runs single local Chrome instance."""
    logger.info("=== Running Framework in LOCAL Mode ===")
    driver = DriverFactory.create_local_driver("chrome")
    try:
        scraper = ElPaisScraper(driver)
        translator = DeepTranslatorService()
        analyzer = WordFrequencyAnalyzer()
        pipeline = ArticlePipeline(scraper, translator, analyzer)

        articles, repeated_words = pipeline.execute(
            section_name=settings.TARGET_SECTION,
            limit=settings.SCRAPE_LIMIT
        )

        ReportGenerator.generate_json_report(articles, repeated_words, session_name="Local_Chrome")
        ReportGenerator.generate_text_summary(articles, repeated_words)
        logger.info("=== Local Mode Execution Finished ===")
    finally:
        driver.quit()


def run_parallel_browserstack_mode():
    """Runs 5 concurrent threads across BrowserStack Desktop & Real Mobile Grid."""
    logger.info("=== Running Framework in BROWSERSTACK PARALLEL Mode (5 Threads) ===")
    capabilities = get_browserstack_capabilities()

    results = []
    # Concurrency Management via ThreadPoolExecutor
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_cap = {
            executor.submit(execute_pipeline_on_capability, cap): cap for cap in capabilities
        }
        for future in concurrent.futures.as_completed(future_to_cap):
            res = future.result()
            results.append(res)

    # Process reports from the first successful session
    successful_runs = [r for r in results if r["status"] == "passed"]
    if successful_runs:
        primary_run = successful_runs[0]
        ReportGenerator.generate_json_report(
            primary_run["articles"],
            primary_run["repeated_words"],
            session_name="BrowserStack_Parallel"
        )
        ReportGenerator.generate_text_summary(
            primary_run["articles"],
            primary_run["repeated_words"]
        )
        logger.info("📊 Parallel execution reports successfully exported.")
    else:
        logger.error("⚠️ All parallel sessions failed. Review execution.log for details.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BrowserStack El País Scraper CLI Framework")
    parser.add_argument(
        "--mode",
        choices=["local", "parallel"],
        default="parallel",
        help="Execution mode: 'local' for local browser or 'parallel' for BrowserStack Cloud Grid."
    )
    args = parser.parse_args()

    if args.mode == "local":
        run_local_mode()
    else:
        run_parallel_browserstack_mode()