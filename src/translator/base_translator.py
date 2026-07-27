from abc import ABC, abstractmethod


class BaseTranslator(ABC):

    @abstractmethod
    def translate_text(
        self, text: str, source_lang: str = "es", target_lang: str = "en"
    ) -> str:
        """Translates text from source_lang to target_lang."""
        pass
