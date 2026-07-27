from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from src.config.settings import settings
from src.utils.logger import logger


class DriverFactory:

    @staticmethod
    def create_local_driver(browser_name: str = "chrome") -> WebDriver:
        """Instantiates a local Chrome or Firefox WebDriver instance."""
        logger.info(f"Initializing local WebDriver: {browser_name}")
        if browser_name.lower() == "chrome":
            options = webdriver.ChromeOptions()
            driver = webdriver.Chrome(options=options)
        elif browser_name.lower() == "firefox":
            options = webdriver.FirefoxOptions()
            driver = webdriver.Firefox(options=options)
        else:
            raise ValueError(f"Unsupported local browser: {browser_name}")

        driver.maximize_window()
        return driver

    @staticmethod
    def create_remote_driver(capability: dict) -> WebDriver:
        """Instantiates Remote WebDriver connected to BrowserStack."""
        logger.info("Connecting Remote WebDriver to BrowserStack Grid...")

        browser_name = capability.get("browserName", "").lower()
        if "safari" in browser_name:
            options = webdriver.SafariOptions()
        elif "firefox" in browser_name:
            options = webdriver.FirefoxOptions()
        else:
            options = webdriver.ChromeOptions()

        for key, value in capability.items():
            if key == "bstack:options":
                options.set_capability("bstack:options", value)
            else:
                options.set_capability(key, value)

        driver = webdriver.Remote(
            command_executor=settings.BROWSERSTACK_URL, options=options
        )
        return driver
