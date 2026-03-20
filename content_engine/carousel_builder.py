import anthropic
import csv
import json
import os
from datetime import date


def run_educational_carousels(client: anthropic.Anthropic, output_dir: str = "output") -> list[dict]:
    """
    Agent 2a: Generates 2 educational carousel ideas per day.
    Topics: SQL, Python, AI, ML, Stats, Power BI, Data Viz, Career in data.
    5 slides each. Content in Spanish.
    """
    today = date.today().isoformat()

    prompt = """Genera EXACTAMENTE 2 ideas de carrusel educativo para Instagram/TikTok sobre datos y tecnología.
El contenido debe ser en ESPAÑOL, claro y útil para personas que están aprendiendo sobre datos, Python, SQL o IA.

Categorías posibles: SQL, Python, Machine Learning, Estadística, Power BI, Excel para datos,
Inteligencia Artificial, ChatGPT/LLMs, Data Visualization, Carrera en datos.

Cada carrusel tiene EXACTAMENTE 5 slides. Devuelve SOLO este JSON:
{
    "educational_carousels": [
        {
            "topic": "tema del carrusel",
            "category": "SQL/Python/IA/ML/etc.",
            "slide_1_cover": "Título impactante del cover (máx 10 palabras, con gancho fuerte)",
            "slide_2_content": "Slide 2: concepto o problema (máx 50 palabras, directo y claro)",
            "slide_3_content": "Slide 3: explicación o ejemplo práctico (máx 50 palabras)",
            "slide_4_content": "Slide 4: tip clave o caso real (máx 50 palabras)",
            "slide_5_cta": "Slide 5: call to action (máx 20 palabras, invita a guardar o seguir)",
            "caption": "Caption para el post en español (máx 100 palabras, con pregunta al final)",
            "hashtags": "#hashtag1 #hashtag2 #hashtag3 #hashtag4 #hashtag5 #hashtag6 #hashtag7 #hashtag8"
        }
    ]
}"""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )

    text = next((b.text for b in response.content if hasattr(b, "text")), "")

    try:
        start = text.find("{")
        end = text.rfind("}") + 1
        data = json.loads(text[start:end])
        carousels = data.get("educational_carousels", [])
    except (json.JSONDecodeError, ValueError):
        print("Error al parsear los carruseles educativos.")
        carousels = []

    os.makedirs(output_dir, exist_ok=True)
    csv_path = os.path.join(output_dir, f"educational_carousels_{today}.csv")

    if carousels:
        fieldnames = [
            "date", "topic", "category",
            "slide_1_cover", "slide_2_content", "slide_3_content",
            "slide_4_content", "slide_5_cta",
            "caption", "hashtags",
        ]
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for c in carousels:
                c["date"] = today
                writer.writerow({k: c.get(k, "") for k in fieldnames})
        print(f"Carruseles educativos guardados en: {csv_path}")

    return carousels


def run_news_carousels(client: anthropic.Anthropic, output_dir: str = "output") -> list[dict]:
    """
    Agent 2b: Searches for the 3 latest AI/data news and generates carousel content.
    5 slides each. Content in Spanish.
    """
    today = date.today().isoformat()

    prompt = f"""Busca en internet las 3 noticias más importantes de HOY ({today}) sobre:
- Inteligencia Artificial (nuevos modelos, lanzamientos, actualizaciones de OpenAI, Anthropic, Google, Meta, etc.)
- Data Science o Big Data
- Machine Learning
- Herramientas o librerías de Python para datos

Luego crea un carrusel de Instagram de 5 slides para cada noticia en ESPAÑOL.

Devuelve EXACTAMENTE este JSON (solo el JSON, sin texto adicional):
{{
    "news_carousels": [
        {{
            "headline": "titular de la noticia en español",
            "source": "fuente de la noticia (sitio web)",
            "slide_1_cover": "Título impactante para el cover (máx 10 palabras, con gancho)",
            "slide_2_content": "Slide 2: ¿Qué pasó? (resumen en máx 50 palabras)",
            "slide_3_content": "Slide 3: ¿Por qué importa? (impacto en máx 50 palabras)",
            "slide_4_content": "Slide 4: ¿Qué significa para ti? (aplicación práctica, máx 50 palabras)",
            "slide_5_cta": "Slide 5: call to action (máx 20 palabras)",
            "caption": "Caption para Instagram/TikTok en español (máx 100 palabras, con pregunta al final)",
            "hashtags": "#hashtag1 #hashtag2 #hashtag3 #hashtag4 #hashtag5 #hashtag6 #hashtag7 #hashtag8"
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
        carousels = data.get("news_carousels", [])
    except (json.JSONDecodeError, ValueError):
        print("Error al parsear los carruseles de noticias.")
        carousels = []

    os.makedirs(output_dir, exist_ok=True)
    csv_path = os.path.join(output_dir, f"news_carousels_{today}.csv")

    if carousels:
        fieldnames = [
            "date", "headline", "source",
            "slide_1_cover", "slide_2_content", "slide_3_content",
            "slide_4_content", "slide_5_cta",
            "caption", "hashtags",
        ]
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for c in carousels:
                c["date"] = today
                writer.writerow({k: c.get(k, "") for k in fieldnames})
        print(f"Carruseles de noticias guardados en: {csv_path}")

    return carousels
