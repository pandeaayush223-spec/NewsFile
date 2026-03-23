import json
from groq import Groq
from config import TOPICS, GROQ_API_KEY
from logger import get_logger

logger = get_logger(__name__)

client = Groq(api_key=GROQ_API_KEY)

# Build topic list string once at import time
_TOPICS_TEXT = "\n".join(
    f"  {parent}: {', '.join(subtopics)}"
    for parent, subtopics in TOPICS.items()
    if subtopics
)

def groq_classify(title: str, summary: str) -> tuple[str, str | None]:
    """Use Groq to classify an article into topic and subtopic."""
    try:
        system = (
            "You are a news article classifier. Given an article, return ONLY a JSON object "
            "with no markdown and no explanation.\n"
            "Use exactly one of these topics and subtopics:\n"
            f"{_TOPICS_TEXT}\n"
            'Return format: {"topic": "ParentTopic", "subtopic": "Subtopic"}\n'
            'If the article does not fit any topic, return {"topic": "Other", "subtopic": null}'
        )
        user = f"Title: {title}\n\nSummary: {summary[:300]}"

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        )

        raw = response.choices[0].message.content.strip()
        result = json.loads(raw)

        topic = result.get("topic", "Other")
        subtopic = result.get("subtopic")

        # Validate against TOPICS dict
        valid_subtopics = TOPICS.get(topic, [])
        if topic not in TOPICS or (subtopic is not None and subtopic not in valid_subtopics):
            logger.warning(f"Groq returned invalid topic/subtopic: {topic!r}/{subtopic!r}")
            return "Other", None

        return topic, subtopic

    except Exception as e:
        logger.error(f"Groq classify error for '{title[:50]}': {e}")
        return "Other", None
