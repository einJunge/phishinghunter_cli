import requests
from datetime import datetime  # ✅ <-- Agregado
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def enviar_reporte_telegram(dominio_sospechoso: str, detalle: str, virustotal_url: str = None) -> None:
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
    mensaje = (
        f"🚨 <b>Alerta de Certificado Sospechoso Detectado</b> 🚨\n\n"
        f"🔗 <b>ID del Dominio objetivo:</b> {TELEGRAM_CHAT_ID}\n"
        f"⚠️ <b>Dominio sospechoso:</b> <code>{dominio_sospechoso}</code>\n"
        f"📅 <b>Detectado en:</b> {timestamp}\n\n"
        f"📝 <b>Detalles:</b>\n{detalle}\n"
    )
    if virustotal_url:
        mensaje += f"\n🔍 <a href='{virustotal_url}'>Ver reporte VirusTotal</a>"

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mensaje,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }

    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        print("[✔️] Reporte enviado a Telegram correctamente.")
    except requests.exceptions.RequestException as e:
        print(f"[❌] Error al enviar reporte a Telegram: {e}")

