import pytest
from src.analyzer.text_analyzer import WordFrequencyAnalyzer

def test_repeated_words_threshold():
    analyzer = WordFrequencyAnalyzer()
    titles = [
        "Attack on freedom in Berlin",
        "Pending debt with the history of the Sahara",
        "The empire of fire"
    ]
    # Expected: 'the' appears 3 times (> 2 threshold)
    results = analyzer.analyze_repeated_words(titles, threshold=2)
    assert "the" in results
    assert results["the"] == 3

def test_repeated_words_empty():
    analyzer = WordFrequencyAnalyzer()
    results = analyzer.analyze_repeated_words([], threshold=2)
    assert results == {}