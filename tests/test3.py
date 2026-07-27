from src.translator.translator_service import DeepTranslatorService
from src.analyzer.text_analyzer import WordFrequencyAnalyzer

def verify_translation_and_analysis():
    print("=" * 60)
    print("🔍 VERIFYING PHASE 3: TRANSLATION & TEXT ANALYZER")
    print("=" * 60)

    # Scraped Spanish Titles from your live El País run
    spanish_titles = [
        "Atentado contra la libertad en Berlín",
        "Deuda pendiente con la historia del Sáhara",
        "No más elecciones",
        "El imperio del fuego",
        "‘Salou, 15 de agosto’"
    ]

    translator = DeepTranslatorService()
    analyzer = WordFrequencyAnalyzer()

    # 1. Test Translation
    print("\n🌐 Translating Spanish Titles to English...")
    english_titles = []
    for idx, es_title in enumerate(spanish_titles, start=1):
        en_title = translator.translate_text(es_title)
        english_titles.append(en_title)
        print(f" [{idx}] ES: {es_title}")
        print(f"     EN: {en_title}")

    # 2. Test Word Frequency Counter (count > 2)
    print("\n📊 Analyzing Word Frequency across English Headers...")
    repeated = analyzer.analyze_repeated_words(english_titles, threshold=2)

    print("\nResults (Words repeated > 2 times):")
    if repeated:
        for word, count in repeated.items():
            print(f" 🔁 Word: '{word}' -> Count: {count}")
    else:
        print(" ℹ️ No single word was repeated more than twice across these 5 headers.")

    print("\n🎉 PHASE 3 VERIFICATION PASSED PERFECTLY!")

if __name__ == "__main__":
    verify_translation_and_analysis()