from typing import List, Dict, Any


def get_browserstack_capabilities() -> List[Dict[str, Any]]:
    """
    Returns a matrix of 5 distinct W3C-compliant capabilities
    for cross-browser desktop and real mobile device testing.
    """
    return [
        {
            "browserName": "Chrome",
            "browserVersion": "latest",
            "bstack:options": {
                "os": "Windows",
                "osVersion": "11",
                "sessionName": "Parallel Thread 1 - Chrome Windows",
                "projectName": "El Pais Scraper",
                "buildName": "BrowserStack CE Assignment",
            },
        },
        {
            "browserName": "Safari",
            "browserVersion": "latest",
            "bstack:options": {
                "os": "OS X",
                "osVersion": "Sonoma",
                "sessionName": "Parallel Thread 2 - Safari Mac",
                "projectName": "El Pais Scraper",
                "buildName": "BrowserStack CE Assignment",
            },
        },
        {
            "browserName": "Firefox",
            "browserVersion": "latest",
            "bstack:options": {
                "os": "Windows",
                "osVersion": "10",
                "sessionName": "Parallel Thread 3 - Firefox Windows",
                "projectName": "El Pais Scraper",
                "buildName": "BrowserStack CE Assignment",
            },
        },
        {
            "bstack:options": {
                "deviceName": "iPhone 15",
                "osVersion": "17",
                "realMobile": "true",
                "sessionName": "Parallel Thread 4 - iOS Mobile",
                "projectName": "El Pais Scraper",
                "buildName": "BrowserStack CE Assignment",
            }
        },
        {
            "bstack:options": {
                "deviceName": "Samsung Galaxy S24",
                "osVersion": "14.0",
                "realMobile": "true",
                "sessionName": "Parallel Thread 5 - Android Mobile",
                "projectName": "El Pais Scraper",
                "buildName": "BrowserStack CE Assignment",
            }
        },
    ]
