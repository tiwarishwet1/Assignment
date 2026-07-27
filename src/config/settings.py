import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    # BrowserStack Credentials
    BROWSERSTACK_USERNAME: str = os.getenv(
        "BROWSERSTACK_USERNAME", "YOUR_USERNAME"
    )
    BROWSERSTACK_ACCESS_KEY: str = os.getenv(
        "BROWSERSTACK_ACCESS_KEY", "YOUR_ACCESS_KEY"
    )
    BROWSERSTACK_URL: str = (
        f"https://{BROWSERSTACK_USERNAME}:{BROWSERSTACK_ACCESS_KEY}"
        "@hub-cloud.browserstack.com/wd/hub"
    )

    # Execution Timeouts & Limits
    IMPLICIT_WAIT: int = 10
    EXPLICIT_WAIT: int = 10
    SCRAPE_LIMIT: int = 5

    # Target Configuration
    TARGET_SECTION: str = "opinion"

    # Paths
    OUTPUT_DIR: str = "output"
    IMAGE_DIR: str = os.path.join(OUTPUT_DIR, "images")


settings = Settings()
