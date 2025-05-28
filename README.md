# 🛡️ PhishingHunter

PhishingHunter es una herramienta avanzada para detectar dominios sospechosos que intentan suplantar una organización (como *tudominio.com*) utilizando certificados SSL públicos. Escanea tanto en tiempo real como de forma histórica, realiza análisis en VirusTotal y revisa el contenido web en busca de señales de phishing.

---
██████╗ ██╗  ██╗██╗███████╗██╗  ██╗██╗███╗   ██╗ ██████╗ ██╗  ██╗████████╗███████╗██████╗ 
██╔══██╗██║  ██║██║██╔════╝██║  ██║██║████╗  ██║██╔═══██╗██║  ██║╚══██╔══╝██╔════╝██╔══██╗
██████╔╝███████║██║███████╗███████║██║██╔██╗ ██║██║   ██║███████║   ██║   █████╗  ██████╔╝
██╔═══╝ ██╔══██║██║╚════██║██╔══██║██║██║╚██╗██║██║   ██║██╔══██║   ██║   ██╔══╝  ██╔══██╗
██║     ██║  ██║██║███████║██║  ██║██║██║ ╚████║╚██████╔╝██║  ██║   ██║   ███████╗██║  ██║
╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝

---

## 🚀 Características

- 🕵️‍♂️ Monitor en tiempo real de certificados SSL usando CertStream
- 🕰️ Escaneo histórico de certificados con crt.sh
- 🧠 Verificación automática en VirusTotal
- 🌐 Análisis de contenido HTML con Selenium
- 💬 Alertas automáticas vía Telegram
- 🔁 Sistema de reintentos en caso de errores de conexión
- 📦 Cache para evitar reportes duplicados

---

## ⚙️ Requisitos

- Python 3.8+
- Google Chrome y chromedriver instalados
- API... Cuenta gratuita o premium de [VirusTotal](https://virustotal.com)
- Bot de Telegram creado desde [@BotFather](https://t.me/botfather)

---

## 📦 Instalación

```bash
git clone https://github.com/einJunge/phishinghunter_cli.git
cd phishinghunter_cli
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt


## 📦 Variables de entorno
Crea un archivo .env con el siguiente contenido:

TELEGRAM_BOT_TOKEN=tu_token_de_bot
TELEGRAM_CHAT_ID=tu_chat_id
VIRUSTOTAL_API_KEY=tu_api_key_de_virustotal
TARGET_DOMAIN=tudominio.com
