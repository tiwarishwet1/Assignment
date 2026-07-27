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
