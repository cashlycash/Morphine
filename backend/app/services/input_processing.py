import re
from urllib.parse import urlparse


def normalize_input(content: str, input_type: str) -> dict:
    cleaned = content.strip()
    metadata: dict[str, str | int] = {
        "input_type": input_type,
        "char_count": len(cleaned),
    }
    if input_type == "url":
        parsed = urlparse(cleaned)
        metadata["domain"] = parsed.netloc
    hashtags = re.findall(r"#\w+", cleaned)
    metadata["hashtags_detected"] = len(hashtags)
    return {"normalized_content": cleaned, "metadata": metadata}
