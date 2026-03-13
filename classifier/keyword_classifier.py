from config import TOPICS, TOPIC_KEYWORDS

def classify_article(title: str, summary: str) -> str:
    text = (title + " " + summary).lower()
    scores = {}
    for topic in TOPICS:
        scores[topic] = 0
        
        
    for topic, keywords in TOPIC_KEYWORDS.items():
        for keyword in keywords:
            if keyword.lower() in text:
                scores[topic] += 1
    
    return max(scores, key=lambda topic: scores[topic])