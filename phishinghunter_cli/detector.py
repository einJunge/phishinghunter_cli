import time
from datetime import datetime
import json
import os
import config
from telegram_alert import enviar_reporte_telegram
from vt_lookup import check_domain_virustotal
from web_analyzer import analyze_website
from utils import setup_logger

logger = setup_logger()

CACHE_FILE = "report_cache.json"
_REPORT_COOLDOWN = 3600  # 1 hora en segundos

def cargar_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    return {}

def guardar_cache(cache):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f)

_report_cache = cargar_cache()

def puede_reportar(dominio):
    ahora = time.time()
    if dominio in _report_cache and (ahora - _report_cache[dominio] < _REPORT_COOLDOWN):
        return False
    _report_cache[dominio] = ahora
    guardar_cache(_report_cache)
    return True

def analizar_certificado(certificado, dominio_sospechoso):
    subject = certificado.get("subject", "N/A")
    issuer = certificado.get("issuer", "N/A")
    not_before = certificado.get("not_before", "N/A")
    not_after = certificado.get("not_after", "N/A")

    detalle = (
        f"Subject: {subject}\n"
        f"Issuer: {issuer}\n"
        f"Fecha emisión: {not_before}\n"
        f"Fecha expiración: {not_after}"
    )

    # Chequeo en VirusTotal
    vt_score = check_domain_virustotal(dominio_sospechoso)
    logger.info(f"VirusTotal score para {dominio_sospechoso}: {vt_score}")

    # Análisis web
    web_score = analyze_website(dominio_sospechoso)
    logger.info(f"Puntaje análisis web para {dominio_sospechoso}: {web_score}")

    # Decisión de reporte
    if vt_score > 0 or web_score >= 2:
        vt_url = f"https://www.virustotal.com/gui/domain/{dominio_sospechoso}/detection"
        enviar_reporte_telegram(dominio_sospechoso, detalle, vt_url)
        logger.info(f"Reporte enviado para {dominio_sospechoso}")
    else:
        logger.info(f"No se reporta {dominio_sospechoso} por bajo riesgo (VT: {vt_score}, Web: {web_score})")

def procesar_certificado_sospechoso(certificado, dominio_sospechoso):
    logger.warning(f"Certificado sospechoso detectado: {dominio_sospechoso}")
    if puede_reportar(dominio_sospechoso):
        analizar_certificado(certificado, dominio_sospechoso)
    else:
        logger.info(f"Dominio {dominio_sospechoso} ya reportado recientemente, evitando duplicados.")

