from app.schemas.common import OutputFormat, TransformParameters


def generate_linkedin(text: str, params: TransformParameters) -> dict:
    snippet = text[:240].strip()
    post = f"{snippet}..." if len(text) > 240 else snippet
    return {
        "post_text": post,
        "hashtags": ["#AI", "#Content", "#Automation"],
        "cta": "What would you transform first?",
        "carousel_slides": [post],
        "tone": params.tone,
    }


def generate_twitter(text: str, params: TransformParameters) -> dict:
    chunks = [text[i : i + 240] for i in range(0, min(len(text), 1200), 240)] or [text]
    tweets = [
        {
            "thread_order": idx + 1,
            "text": chunk,
            "engagement_score": 0.75,
        }
        for idx, chunk in enumerate(chunks)
    ]
    return {"tweets": tweets, "style": params.style}


def generate_summary(text: str, params: TransformParameters) -> dict:
    words = text.split()
    summary = " ".join(words[: min(len(words), 150)])
    return {
        "sections": ["Overview", "Key Takeaways", "Action Items", "Risks", "Next Steps"],
        "markdown": summary,
        "key_takeaways": ["Faster repurposing", "Consistent tone", "Lower cost"],
        "action_items": ["Review output", "Publish selected formats"],
        "detail_level": params.detail_level,
    }


def generate_video_script(text: str, params: TransformParameters) -> dict:
    lines = [line for line in text.split(".") if line.strip()][:5]
    return {
        "script": "\n".join(f"Narrator: {line.strip()}." for line in lines) or f"Narrator: {text}",
        "scenes": [{"scene": i + 1, "description": line.strip()} for i, line in enumerate(lines)],
        "timing": {"estimated_seconds": max(30, len(text.split()) // 2)},
        "subtitles": "1\n00:00:00,000 --> 00:00:03,000\nIntro\n",
        "music_cues": ["Intro ambient at 0:00"],
        "transitions": ["fade"],
        "audience": params.audience,
    }


def generate_for_format(fmt: OutputFormat, text: str, params: TransformParameters) -> dict:
    if fmt == OutputFormat.linkedin:
        return generate_linkedin(text, params)
    if fmt == OutputFormat.twitter:
        return generate_twitter(text, params)
    if fmt == OutputFormat.executive_summary:
        return generate_summary(text, params)
    return generate_video_script(text, params)
