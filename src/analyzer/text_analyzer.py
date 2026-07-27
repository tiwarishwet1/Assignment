import re
from collections import Counter
from typing import List, Dict
from src.analyzer.base_analyzer import BaseAnalyzer
from src.utils.logger import logger


class WordFrequencyAnalyzer(BaseAnalyzer):

    def analyze_repeated_words(
        self, titles: List[str], threshold: int = 2
    ) -> Dict[str, int]:
        all_words = []

        for title in titles:
            if not title or title == "Translation Unavailable":
                continue
            # Extract alphanumeric words and normalize to lower case
            words = re.findall(r"\b\w+\b", title.lower())
            all_words.extend(words)

        counts = Counter(all_words)

        # Filter words repeated STRICTLY MORE THAN THRESHOLD times
        repeated_words = {
            word: count for word, count in counts.items() if count > threshold
        }

        logger.info(
            f"Analyzed {len(all_words)} total words across headers. "
            f"Found {len(repeated_words)} repeated > {threshold} times."
        )
        return repeated_words
