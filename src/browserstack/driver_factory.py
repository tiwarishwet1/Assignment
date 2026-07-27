from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from src.utils.logger import logger


class DriverFactory:

    @staticmethod
    def create_driver() -> WebDriver:
        """
        Instantiates WebDriver.
        When invoked via `browserstack-sdk`, the SDK intercepts
        this call and connects to the BrowserStack Cloud Grid automatically.
        """
        logger.info("Initializing WebDriver session via BrowserStack SDK...")
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(options=options)

        # Safely maximize window (ignored on mobile viewports/Android/iOS)
        try:
            driver.maximize_window()
        except Exception:
            logger.debug("Window maximize skipped (Mobile Viewport detected).")

        return driver