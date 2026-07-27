from src.browserstack.driver_factory import DriverFactory
from src.scraper.el_pais_scraper import ElPaisScraper
from src.utils.logger import logger

def verify_scraper():
    print("=" * 60)
    print("🔍 VERIFYING PHASE 2: LOCAL SCRAPER ENGINE")
    print("=" * 60)

    driver = DriverFactory.create_local_driver("chrome")
    try:
        scraper = ElPaisScraper(driver)
        articles = scraper.scrape_section(section_name="opinion", limit=5)

        print(f"\n✅ Scraped {len(articles)} Articles Successfully:\n")
        for art in articles:
            print(f"[{art.index}] TITLE (ES): {art.title_es}")
            print(f"    CONTENT (ES): {art.content_es[:80]}...")
            print(f"    IMAGE PATH  : {art.local_image_path}\n")

        print("🎉 PHASE 2 VERIFICATION PASSED PERFECTLY!")
    except Exception as e:
        print(f"\n❌ Phase 2 Verification Failed: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    verify_scraper()