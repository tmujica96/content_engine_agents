import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import date


def build_html_email(trending: list[dict], edu: list[dict], news: list[dict]) -> str:
    today = date.today().strftime("%d %B %Y")

    html = f"""
    <html><body style="font-family: Arial, sans-serif; max-width: 700px; margin: auto; color: #222;">

    <h1 style="background:#1a1a2e; color:white; padding:20px; border-radius:8px;">
        📊 datacontomas — Contenido del día<br>
        <span style="font-size:16px; font-weight:normal;">{today}</span>
    </h1>

    <!-- TRENDING TOPICS -->
    <h2 style="color:#e94560; border-bottom: 2px solid #e94560; padding-bottom:6px;">
        🔥 Temas Trending (para Reels)
    </h2>
    <table style="width:100%; border-collapse:collapse;">
        <tr style="background:#f5f5f5;">
            <th style="padding:8px; text-align:left;">Tema</th>
            <th style="padding:8px; text-align:left;">Plataforma</th>
            <th style="padding:8px; text-align:left;">Ángulo para Reel</th>
            <th style="padding:8px; text-align:left;">Dificultad</th>
        </tr>
    """
    for i, t in enumerate(trending):
        bg = "#ffffff" if i % 2 == 0 else "#f9f9f9"
        html += f"""
        <tr style="background:{bg};">
            <td style="padding:8px; font-weight:bold;">{t.get('topic', '')}</td>
            <td style="padding:8px;">{t.get('platform', '')}</td>
            <td style="padding:8px;">{t.get('reel_angle', '')}</td>
            <td style="padding:8px;">{t.get('difficulty', '')}</td>
        </tr>"""

    html += "</table>"

    # EDUCATIONAL CAROUSELS
    html += """
    <h2 style="color:#0f3460; border-bottom: 2px solid #0f3460; padding-bottom:6px; margin-top:30px;">
        📚 Carruseles Educativos (2 ideas)
    </h2>"""

    for i, c in enumerate(edu, 1):
        html += f"""
    <div style="border:1px solid #ddd; border-radius:8px; padding:16px; margin-bottom:16px;">
        <h3 style="margin:0 0 10px 0; color:#0f3460;">
            #{i} [{c.get('category', '')}] {c.get('topic', '')}
        </h3>
        <table style="width:100%; border-collapse:collapse;">
            <tr><td style="padding:6px 8px; background:#e8f4fd; font-weight:bold; width:30%;">Slide 1 — Cover</td>
                <td style="padding:6px 8px;">{c.get('slide_1_cover', '')}</td></tr>
            <tr><td style="padding:6px 8px; background:#f0f8ff; font-weight:bold;">Slide 2</td>
                <td style="padding:6px 8px;">{c.get('slide_2_content', '')}</td></tr>
            <tr><td style="padding:6px 8px; background:#e8f4fd; font-weight:bold;">Slide 3</td>
                <td style="padding:6px 8px;">{c.get('slide_3_content', '')}</td></tr>
            <tr><td style="padding:6px 8px; background:#f0f8ff; font-weight:bold;">Slide 4</td>
                <td style="padding:6px 8px;">{c.get('slide_4_content', '')}</td></tr>
            <tr><td style="padding:6px 8px; background:#e8f4fd; font-weight:bold;">Slide 5 — CTA</td>
                <td style="padding:6px 8px;">{c.get('slide_5_cta', '')}</td></tr>
        </table>
        <p style="margin-top:10px; font-size:13px; color:#555;">
            <strong>Caption:</strong> {c.get('caption', '')}<br>
            <strong>Hashtags:</strong> <span style="color:#0f3460;">{c.get('hashtags', '')}</span>
        </p>
    </div>"""

    # NEWS CAROUSELS
    html += """
    <h2 style="color:#16213e; border-bottom: 2px solid #e94560; padding-bottom:6px; margin-top:30px;">
        📰 Noticia de IA & Data
    </h2>"""

    for i, c in enumerate(news, 1):
        html += f"""
    <div style="border:1px solid #ddd; border-radius:8px; padding:16px; margin-bottom:16px; border-left: 4px solid #e94560;">
        <h3 style="margin:0 0 4px 0; color:#e94560;">{c.get('headline', '')}</h3>
        <p style="margin:0 0 10px 0; font-size:12px; color:#888;">Fuente: {c.get('source', '')}</p>
        <table style="width:100%; border-collapse:collapse;">
            <tr><td style="padding:6px 8px; background:#fff0f0; font-weight:bold; width:30%;">Slide 1 — Cover</td>
                <td style="padding:6px 8px;">{c.get('slide_1_cover', '')}</td></tr>
            <tr><td style="padding:6px 8px; background:#fff8f8; font-weight:bold;">Slide 2 — Qué pasó</td>
                <td style="padding:6px 8px;">{c.get('slide_2_content', '')}</td></tr>
            <tr><td style="padding:6px 8px; background:#fff0f0; font-weight:bold;">Slide 3 — Por qué importa</td>
                <td style="padding:6px 8px;">{c.get('slide_3_content', '')}</td></tr>
            <tr><td style="padding:6px 8px; background:#fff8f8; font-weight:bold;">Slide 4 — Para ti</td>
                <td style="padding:6px 8px;">{c.get('slide_4_content', '')}</td></tr>
            <tr><td style="padding:6px 8px; background:#fff0f0; font-weight:bold;">Slide 5 — CTA</td>
                <td style="padding:6px 8px;">{c.get('slide_5_cta', '')}</td></tr>
        </table>
        <p style="margin-top:10px; font-size:13px; color:#555;">
            <strong>Caption:</strong> {c.get('caption', '')}<br>
            <strong>Hashtags:</strong> <span style="color:#e94560;">{c.get('hashtags', '')}</span>
        </p>
    </div>"""

    html += """
    <p style="text-align:center; color:#aaa; font-size:12px; margin-top:30px;">
        Generado automáticamente por el Content Engine de datacontomas 🤖
    </p>
    </body></html>"""

    return html


def send_email(trending: list[dict], edu: list[dict], news: list[dict]):
    """Sends the daily content digest to tomasmujica96@gmail.com via Gmail SMTP."""

    gmail_user = os.environ["GMAIL_USER"]
    gmail_password = os.environ["GMAIL_APP_PASSWORD"]
    recipient = "tomasmujica96@gmail.com"

    today = date.today().strftime("%d %b %Y")
    subject = f"📊 datacontomas — Contenido del día {today}"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = gmail_user
    msg["To"] = recipient

    html_content = build_html_email(trending, edu, news)
    msg.attach(MIMEText(html_content, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, recipient, msg.as_string())

    print(f"Email enviado a {recipient}")
