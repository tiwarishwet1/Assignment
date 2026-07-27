from abc import ABC, abstractmethod
from typing import List, Dict


class BaseAnalyzer(ABC):

    @abstractmethod
    def analyze_repeated_words(
        self, titles: List[str], threshold: int = 2
    ) -> Dict[str, int]:
        """Analyzes titles and returns words repeated > threshold times."""
        pass
