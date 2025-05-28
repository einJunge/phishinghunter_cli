# 🛡️ PhishingHunter_cli

PhishingHunter_cli es una herramienta avanzada para detectar dominios sospechosos que intentan suplantar una organización (como *tudominio.com*) utilizando certificados SSL públicos. Escanea tanto en tiempo real como de forma histórica, realiza análisis en VirusTotal y revisa el contenido web en busca de señales de phishing.

---
![image](https://github.com/user-attachments/assets/4e72772d-0f2e-49fd-996e-4be092204a70)



---
📄 Licencia
MIT License - 2025 - [Marcos Hernandez | grep "Ascitgroup.com"]

🤝 Contribuciones
¡Pull Requests y mejoras son bienvenidas! 🙌

🌐 Créditos
Inspirado por iniciativas de OSINT y ciberseguridad comunitaria.

** Dato importante
La herramienta suele tener un incoveniente con el crt.sh error de conexion (suele pasar cuando el trafico de crt.sh es muy lento y rechaza la conexion)
cuando suceda se debe de reiniciar la herramienta



## 📌 Características

- 🔍 **Monitoreo en tiempo real** con CertStream
- 🕘 **Análisis histórico** desde `crt.sh`
- 🧠 **Detección inteligente** con fuzzy matching (`fuzzywuzzy`)
- 🤖 **Alertas automáticas** a Telegram
- 🛡️ **Consulta de reputación** vía API de VirusTotal
- 🌐 **Análisis web automatizado** con Selenium
- 🧪 Modo DEMO disponible
- 🗂️ Uso de caché para evitar reanálisis
- 🔁 Reinicio automático ante fallos críticos
- 🧭 Soporte para ejecución como servicio Linux (`systemd`)
---


## ⚙️ Requisitos

- Python 3.8+
- Google Chrome y chromedriver instalados
- API... Cuenta gratuita o premium de [VirusTotal](https://virustotal.com)
- Bot de Telegram creado desde [@BotFather](https://t.me/botfather)

---
![ChatGPT Image 28 may 2025, 16_14_25](https://github.com/user-attachments/assets/6508718f-68d2-4942-acc9-e5eab7820a78)


## 📦 Instalación

```bash
git clone https://github.com/einJunge/phishinghunter_cli.git
mover la herramienta al directorio de /opt/
cd phishinghunter_cli
mkdir cache logs
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

## 📦 Variables de entorno
Crea un archivo .env con el siguiente contenido:

TELEGRAM_BOT_TOKEN=tu_token_de_bot
TELEGRAM_CHAT_ID=tu_chat_id
VIRUSTOTAL_API_KEY=tu_api_key_de_virustotal
TARGET_DOMAIN=tudominio.com

## 🧪 Modo DEMO vs Producción (config.py)
DEMO_MODE = True: ejecuta análisis histórico + tiempo real.
DEMO_MODE = False: solo monitorea en tiempo real.

## ▶️ Uso Manual
python phishinghunter.py

## 🗃️ Sistema de Caché
La herramienta guarda los dominios ya reportados en cache/historial_reportes.json, evitando duplicados tanto en modo demo como en producción.

🧰 Archivos Importantes
phishinghunter_cli/
├── phishinghunter.py                    # Archivo principal
├── certstream_handler.py     # Monitor en tiempo real
├── historical_search.py      # Escaneo histórico (crt.sh)
├── telegram_alert.py         # Envío a Telegram
├── vt_lookup.py              # Análisis con VirusTotal
├── web_analyzer.py           # Análisis web con Selenium
├── detector.py               # Motor de análisis de certificados
├── config.py                 # Carga .env
├── utils.py                  # Logging y herramientas
├── cache/
│   └── historial_reportes.json
├── .env                      # Variables de entorno (NO subir a GitHub)
├── requirements.txt          # Dependencias
└── README.md                 # Este archivo


## 📷 Ejemplo en consola
🛡️  PhishingHunter - Monitor de Certificados SSL en Tiempo Real
🎯 Dominio objetivo: paypal.com
🔧 Modo Demo: Activado (Histórico + Tiempo real)
⌛ Esperando coincidencias de certificados...


🧩 Ejecutar como Servicio (Linux)
sudo nano /etc/systemd/system/phishinghunterPro.service
--
## Pega el contenido siguiente:
[Unit]
Description=PhishingHunter CLI - Phishing Detector en Tiempo Real (con logs)
After=network.target

[Service]
User=root
WorkingDirectory=/opt/phishinghunter_cli
ExecStart=/opt/phishinghunter_cli/venv/bin/python3 /opt/phishinghunter_cli/phishinghunter.py
StandardOutput=append:/opt/phishinghunter_cli/logs/phishinghunter.log
StandardError=append:/opt/phishinghunter_cli/logs/phishinghunter.log
Restart=on-failure
RestartSec=5
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target

---

## Habilita y ejecuta el servicio:
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable phishinghunter.service
sudo systemctl start phishinghunter.service

## Verifica los logs:
journalctl -u phishinghunter.service -f
tail -f phishinghunterPro.log
---
