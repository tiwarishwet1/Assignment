from deep_translator import GoogleTranslator
from src.translator.base_translator import BaseTranslator
from src.utils.logger import logger


class DeepTranslatorService(BaseTranslator):

    def translate_text(
        self, text: str, source_lang: str = "es", target_lang: str = "en"
    ) -> str:
        if not text or text == "Title Unavailable":
            return "Translation Unavailable"
        try:
            translated = GoogleTranslator(
                source=source_lang, target=target_lang
            ).translate(text)
            return translated
        except Exception as e:
            logger.error(
                f"Translation failed for string '{text[:25]}...': {e}"
            )
            return text
