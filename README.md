# Enterprise El País Web Scraper & Parallel BrowserStack Pipeline

An enterprise-grade, SOLID-compliant Selenium automation framework that scrapes, translates, and analyzes El País opinion articles across 5 parallel Desktop & Mobile threads on BrowserStack Cloud Grid.

## 🏛️ Architecture Overview
- **Design Patterns**: SOLID Principles, Factory Pattern, Dependency Injection, Abstract Base Classes (ABC).
- **Parallel Grid**: `concurrent.futures.ThreadPoolExecutor` managing W3C-compliant capabilities across 5 concurrent cloud sessions.
- **Observability**: Structured JSON telemetry artifacts, formatted TXT summaries, and custom `browserstack_executor` dashboard session statuses.

## 🚀 Quickstart

1. **Environment Setup**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Configure Credentials (`.env`)**:
   ```ini
   BROWSERSTACK_USERNAME=your_username
   BROWSERSTACK_ACCESS_KEY=your_access_key
   ```

3. **Execution Modes**:
   - **Local Single Thread**:
     ```bash
     python3 main.py --mode local
     ```
   - **BrowserStack 5-Thread Cloud Parallel Execution**:
     ```bash
     python3 main.py --mode parallel
     ```

4. **Run Unit & Integration Tests**:
   ```bash
   pytest tests/
   ```