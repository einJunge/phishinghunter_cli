import certstream
import config
import time
from detector import procesar_certificado_sospechoso
from utils import setup_logger

logger = setup_logger()

def handle_message(message, context):
    if message['message_type'] == "heartbeat":
        return
    data = message.get("data", {})
    leaf_cert = data.get("leaf_cert", {})
    all_domains = leaf_cert.get("all_domains", [])

    for domain in all_domains:
        if domain.endswith(config.TARGET_DOMAIN):
            procesar_certificado_sospechoso(leaf_cert, domain)

_started = False

def run_certstream_monitor():
    global _started
    if _started:
        logger.info("Monitor ya está corriendo.")
        return
    _started = True
    logger.info("Iniciando monitor en Tiempo real...")

    while True:
        try:
            certstream.listen_for_events(handle_message, url='wss://certstream.calidog.io/')
        except Exception as e:
            logger.error(f"Error en CertStream, intentando reconectar en 5 segundos: {e}")
            time.sleep(5)

