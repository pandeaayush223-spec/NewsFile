from classifier.keyword_classifier import classify_article as keyword_classify
from classifier.groq_classifier import groq_classify
from logger import get_logger

logger = get_logger(__name__)

def classify(title: str, summary: str) -> tuple[str, str | None]:
    """
    Hybrid classifier:
    1. Try keyword classifier first (fast, free)
    2. If confidence is low (returns None, None), fall back to Groq
    """
    topic, subtopic = keyword_classify(title, summary)

    if topic is None:
        logger.debug(f"Low keyword confidence for '{title[:50]}' — falling back to Groq")
        topic, subtopic = groq_classify(title, summary)
    else:
        logger.debug(f"Keyword classified '{title[:50]}' → {topic} / {subtopic}")

    return topic, subtopic
