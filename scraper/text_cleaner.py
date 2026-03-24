from bs4 import BeautifulSoup

_BOILERPLATE = [
    "please enable js", "enable javascript", "ad blocker", "disable your ad",
    "copyright", "all rights reserved", "subscribe", "sign in to read",
]

def clean_html(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")

    for tag_name in ["script", "nav", "style", "footer", "header",
                     "figure", "figcaption", "aside", "picture"]:
        for tag in soup.find_all(tag_name):
            tag.decompose()

    for selector in ["[class*='caption']", "[class*='share']", "[class*='social']",
                     "[class*='byline']", "[class*='credit']"]:
        for tag in soup.select(selector):
            tag.decompose()

    body = soup.find("article") or soup.find("main") or soup.body

    if not body:
        return ""

    paragraphs = []
    seen = set()
    for p in body.find_all("p"):
        text = p.get_text().strip()
        if len(text.split()) < 8:
            continue
        text_lower = text.lower()
        if any(signal in text_lower for signal in _BOILERPLATE):
            continue
        if text not in seen:
            seen.add(text)
            paragraphs.append(text)

    return "\n".join(paragraphs)

def clean_summary(summary: str) -> str:
    if not summary:
        return ""
    soup = BeautifulSoup(summary, "lxml")
    return soup.get_text(separator=" ").strip()
