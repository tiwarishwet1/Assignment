import os
import json
from typing import List, Dict
from dataclasses import asdict

from src.models.article import Article
from src.config.settings import settings
from src.utils.logger import logger


class ReportGenerator:

    @staticmethod
    def generate_json_report(
        articles: List[Article],
        repeated_words: Dict[str, int],
        session_name: str = "Local",
    ) -> str:
        """Generates a structured JSON report artifact."""
        os.makedirs(settings.OUTPUT_DIR, exist_ok=True)

        filename = f"report_{session_name.replace(' ', '_')}.json"
        filepath = os.path.join(settings.OUTPUT_DIR, filename)

        report_data = {
            "session_name": session_name,
            "total_articles": len(articles),
            "articles": [asdict(a) for a in articles],
            "repeated_words_count_gt_2": repeated_words,
        }

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=4, ensure_ascii=False)

        logger.info(f"JSON Report exported to: {filepath}")
        return filepath

    @staticmethod
    def generate_text_summary(
        articles: List[Article], repeated_words: Dict[str, int]
    ) -> str:
        """Generates a human-readable text summary report."""
        os.makedirs(settings.OUTPUT_DIR, exist_ok=True)
        filepath = os.path.join(settings.OUTPUT_DIR, "report_summary.txt")

        lines = [
            "=" * 60,
            "               EL PAÍS SCRAPING & ANALYSIS REPORT",
            "=" * 60,
            f"\nTotal Articles Scraped: {len(articles)}\n",
            "-" * 60,
        ]

        for art in articles:
            lines.append(f"ARTICLE #{art.index}")
            lines.append(f"  Spanish Title   : {art.title_es}")
            lines.append(f"  English Title   : {art.title_en}")
            lines.append(f"  Spanish Content : {art.content_es}")
            lines.append(f"  Cover Image     : {art.local_image_path}")
            lines.append("-" * 60)

        lines.append("\nREPEATED WORDS ANALYSIS (Count > 2):")
        if repeated_words:
            for word, count in repeated_words.items():
                lines.append(f"  • '{word}' -> Occurrences: {count}")
        else:
            lines.append("  • No words repeated > 2 times across headers.")

        lines.append("\n" + "=" * 60)

        summary_content = "\n".join(lines)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(summary_content)

        logger.info(f"Summary Report exported to: {filepath}")
        return summary_content

    @staticmethod
    def generate_html_report(
        articles: List[Article], repeated_words: Dict[str, int]
    ) -> str:
        """Generates an executive visual HTML report."""
        os.makedirs(settings.OUTPUT_DIR, exist_ok=True)
        filepath = os.path.join(settings.OUTPUT_DIR, "report.html")

        cards_html = ""
        for art in articles:
            cards_html += f"""
            <div style="border:1px solid #e0e0e0; border-radius:8px;
                        padding:16px; margin-bottom:16px;
                        font-family:sans-serif; background:#ffffff;">
                <h3 style="color:#1a365d; margin-top:0;">
                    Article #{art.index}
                </h3>
                <p><strong>🇪🇸 Title (ES):</strong> {art.title_es}</p>
                <p><strong>🇬🇧 Title (EN):</strong> {art.title_en}</p>
                <p><strong>📝 Content:</strong> {art.content_es}</p>
                <p><strong>🖼️ Cover Image Path:</strong>
                   <code>{art.local_image_path}</code></p>
            </div>
            """

        badge_style = (
            "background:#e2e8f0; color:#0f172a; padding:6px 14px; "
            "border-radius:16px; font-weight:bold; margin-right:8px; "
            "display:inline-block;"
        )
        msg_no_words = (
            "<span style='color:#64748b;'>"
            "No words repeated > 2 times.</span>"
        )
        word_badges = "".join([
            f'<span style="{badge_style}">{w}: {c}</span>'
            for w, c in repeated_words.items()
        ]) or msg_no_words

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>El País Automation Telemetry Report</title>
            <meta charset="utf-8">
        </head>
        <body style="font-family:sans-serif; background:#f8fafc;
                     max-width:850px; margin:40px auto; padding:0 20px;">
            <h1 style="color:#0f172a;">
                📰 El País Extraction & Analysis Telemetry
            </h1>
            <hr style="border:0; height:1px; background:#cbd5e1;
                       margin-bottom:24px;">
            <h2>📊 Repeated Words Analysis (Count > 2)</h2>
            <div style="margin-bottom:32px;">{word_badges}</div>
            <h2>📑 Scraped Articles ({len(articles)})</h2>
            {cards_html}
        </body>
        </html>
        """

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html_content)

        logger.info(f"HTML Visual Report exported to: {filepath}")
        return filepath
