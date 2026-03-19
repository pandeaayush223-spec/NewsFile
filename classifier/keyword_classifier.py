from config import TOPICS, TOPIC_KEYWORDS

# Build a reverse lookup: subtopic → parent topic (computed once at import time)
_SUBTOPIC_TO_TOPIC = {
    subtopic: parent
    for parent, subtopics in TOPICS.items()
    for subtopic in subtopics
}

def classify_article(title: str, summary: str) -> tuple[str, str | None]:
    """Returns (parent_topic, subtopic). subtopic is None for 'Other'."""
    text = (title + " " + summary).lower()

    scores = {subtopic: 0 for subtopic in _SUBTOPIC_TO_TOPIC}

    for subtopic, keywords in TOPIC_KEYWORDS.items():
        if subtopic == "Other":
            continue
        for keyword in keywords:
            if keyword.lower() in text:
                scores[subtopic] += 1

    best_subtopic = max(scores, key=lambda s: scores[s])

    if scores[best_subtopic] == 0:
        return "Other", None

    parent_topic = _SUBTOPIC_TO_TOPIC.get(best_subtopic, "Other")
    return parent_topic, best_subtopic