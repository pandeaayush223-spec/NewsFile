from config import TOPICS, TOPIC_KEYWORDS

# Build a reverse lookup: subtopic → parent topic (computed once at import time)
_SUBTOPIC_TO_TOPIC = {
    subtopic: parent
    for parent, subtopics in TOPICS.items()
    for subtopic in subtopics
}

def classify_article(title: str, summary: str) -> tuple[str, str | None] | tuple[None, None]:
    """
    Returns (parent_topic, subtopic), or (None, None) if confidence is too low.
    Multi-word keyword phrases score 2 points; single-word keywords score 1 point.
    A minimum score of 2 is required to classify.
    """
    text = (title + " " + summary).lower()

    scores = {subtopic: 0 for subtopic in _SUBTOPIC_TO_TOPIC}

    for subtopic, keywords in TOPIC_KEYWORDS.items():
        if subtopic == "Other":
            continue
        for keyword in keywords:
            if keyword.lower() in text:
                scores[subtopic] += 2 if " " in keyword else 1

    best_subtopic = max(scores, key=lambda s: scores[s])

    if scores[best_subtopic] < 2:
        return None, None

    parent_topic = _SUBTOPIC_TO_TOPIC.get(best_subtopic, "Other")
    return parent_topic, best_subtopic