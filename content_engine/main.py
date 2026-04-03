import anthropic
import time
import os
import sys

# Add parent directory to path so this can be run from anywhere
sys.path.insert(0, os.path.dirname(__file__))

from trend_scout import run_trend_scout
from carousel_builder import run_educational_carousels, run_news_carousels
from email_sender import send_email


def main():
    client = anthropic.Anthropic()
    output_dir = os.path.join(os.path.dirname(__file__), "..", "output")

    print("\n" + "=" * 55)
    print("  datacontomas — Content Engine")
    print("=" * 55)

    # Agent 1: Trend Scout
    print("\n[1/3] TREND SCOUT — Buscando temas trending para reels...")
    topics = run_trend_scout(client, output_dir)
    print(f"      {len(topics)} temas encontrados.")

    if topics:
        print("\n  Temas trending hoy:")
        for i, t in enumerate(topics, 1):
            print(f"  {i}. {t['topic']} ({t['platform']}) — {t['difficulty']}")

    time.sleep(65)  # wait for rate limit window to reset

    # Agent 2a: Educational Carousels
    print("\n[2/3] CAROUSEL EDUCATIVO — Generando 2 ideas...")
    edu = run_educational_carousels(client, output_dir)
    print(f"      {len(edu)} carruseles generados.")

    if edu:
        print("\n  Ideas educativas:")
        for i, c in enumerate(edu, 1):
            print(f"  {i}. [{c['category']}] {c['slide_1_cover']}")

    time.sleep(65)  # wait for rate limit window to reset

    # Agent 2b: News Carousels
    print("\n[3/3] CAROUSEL DE NOTICIAS — Buscando las 3 noticias del dia...")
    news = run_news_carousels(client, output_dir)
    print(f"      {len(news)} carruseles generados.")

    if news:
        print("\n  Noticias de hoy:")
        for i, c in enumerate(news, 1):
            print(f"  {i}. {c['headline']}")

    # Send email digest
    print("\n[EMAIL] Enviando resumen por email...")
    try:
        send_email(topics, edu, news)
    except KeyError as e:
        print(f"      Variable de entorno faltante: {e}. Saltando email.")
    except Exception as e:
        print(f"      Error enviando email: {e}")

    print("\n" + "=" * 55)
    print("  Listo! Revisa la carpeta output/ para tus CSV.")
    print("=" * 55 + "\n")


if __name__ == "__main__":
    main()
