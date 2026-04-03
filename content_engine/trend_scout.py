import anthropic
import csv
import json
import os
from datetime import date


def run_trend_scout(client: anthropic.Anthropic, output_dir: str = "output") -> list[dict]:
    """
    Agent 1: Searches the web for trending topics in data/AI/tech for reels.
    Returns a list of trending topic dicts and saves to CSV.
    """
    today = date.today().isoformat()

    prompt = f"""Busca en internet los temas más trending HOY ({today}) relacionados con:
- Data Science y Analytics
- Python para datos
- SQL
- Inteligencia Artificial (especialmente LLMs, ChatGPT, Claude, Gemini, etc.)
- Machine Learning
- Business Intelligence

Busca en fuentes como Reddit (r/datascience, r/MachineLearning, r/Python, r/artificial),
LinkedIn, YouTube y Twitter/X.

Devuelve EXACTAMENTE 5 temas trending con el siguiente JSON (solo el JSON, sin texto adicional):
{{
    "trending_topics": [
        {{
            "topic": "nombre del tema",
            "platform": "donde es trending (Reddit/LinkedIn/YouTube/Twitter/etc.)",
            "why_trending": "por qué está en tendencia (1-2 oraciones en español)",
            "reel_angle": "ángulo creativo para el reel en español (máximo 15 palabras)",
            "difficulty": "fácil/medio/difícil",
            "hashtags": "#hashtag1 #hashtag2 #hashtag3 #hashtag4 #hashtag5"
        }}
    ]
}}"""

    messages = [{"role": "user", "content": prompt}]
    max_continuations = 5
    continuations = 0

    while continuations < max_continuations:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4096,
            tools=[{"type": "web_search_20260209", "name": "web_search"}],
            messages=messages,
        )

        if response.stop_reason == "end_turn":
            break
        elif response.stop_reason == "pause_turn":
            messages = [
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": response.content},
            ]
            continuations += 1
            continue
        else:
            break

    text = next((b.text for b in response.content if hasattr(b, "text")), "")

    try:
        start = text.find("{")
        end = text.rfind("}") + 1
        data = json.loads(text[start:end])
        topics = data.get("trending_topics", [])
    except (json.JSONDecodeError, ValueError):
        print("Error al parsear los trending topics.")
        topics = []

    os.makedirs(output_dir, exist_ok=True)
    csv_path = os.path.join(output_dir, f"trending_topics_{today}.csv")

    if topics:
        fieldnames = ["date", "topic", "platform", "why_trending", "reel_angle", "difficulty", "hashtags"]
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for t in topics:
                t["date"] = today
                writer.writerow({k: t.get(k, "") for k in fieldnames})
        print(f"Trending topics guardados en: {csv_path}")

    return topics
