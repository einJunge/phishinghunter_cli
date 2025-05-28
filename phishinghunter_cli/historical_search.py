import requests
import time
import os
import logging
import tldextract
from detector import analizar_certificado
from config import TARGET_DOMAIN, DEMO_MODE
from utils import setup_logger
from fuzzywuzzy import fuzz

logger = setup_logger()

CACHE_FILE = "cache/cache_dominios.txt"

def cargar_cache():
    if not os.path.exists(CACHE_FILE):
        return set()
    with open(CACHE_FILE, "r") as f:
        return set(line.strip() for line in f.readlines())

def guardar_cache(cache):
    with open(CACHE_FILE, "w") as f:
        for dominio in cache:
            f.write(dominio + "\n")
##Esta varible suele fallar en algunas ocaciones  cuando no se tiene respuesta del servidor de crt.sh
#Cuando ocurra reinicia la herramienta  hasta que tengas una respuesta
def obtener_certificados_reales(max_retries=6, base_wait=5):
    logger.info("[🌐] Consultando certificados históricos en crt.sh...")
    base = TARGET_DOMAIN.replace("www.", "")
    url = f"https://crt.sh/?q=%.{base}&output=json"
    headers = {
        "User-Agent": "PhishingHunterBot/1.0 (+https://github.com/einJunge/phishinghunter_cli)"
    }

    for intento in range(1, max_retries + 1):
        try:
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code != 200:
                raise Exception(f"Status code: {response.status_code}")
            data = response.json()
            break  # Éxito, salir del ciclo
        except requests.exceptions.RequestException as e:
            logger.error(f"[❌] Error al consultar crt.sh en intento {intento}/{max_retries}: {e}")
            if intento == max_retries:
                logger.error("[❌] Máximo de reintentos alcanzado. No se pudo obtener datos de crt.sh.")
                return []
            sleep_time = base_wait * (2 ** (intento - 1))  # Backoff exponencial
            logger.info(f"Reintentando en {sleep_time} segundos...")
            time.sleep(sleep_time)

    certificados = []
    ya_vistos = set()

    for item in data:
        dominio = item.get("common_name", "").lower()
        if dominio in ya_vistos:
            continue
        ya_vistos.add(dominio)

        cert = {
            "subject": f"CN={dominio}",
            "issuer": item.get("issuer_name", "Desconocido"),
            "not_before": item.get("not_before", "N/A"),
            "not_after": item.get("not_after", "N/A")
        }
        certificados.append((dominio, cert))

    logger.info(f"[✔️] Se recuperaron {len(certificados)} certificados de crt.sh.")
    return certificados

def es_sospechoso(dominio):
    objetivo = TARGET_DOMAIN.lower().replace("www.", "")
    extraido_objetivo = tldextract.extract(objetivo)
    extraido_dominio = tldextract.extract(dominio)

    # Si el dominio extraído es igual al objetivo, no es sospechoso
    if extraido_dominio.registered_domain == extraido_objetivo.registered_domain:
        return False

    # Si contiene el nombre del objetivo pero no es el mismo dominio registrado, es sospechoso
    return extraido_objetivo.domain in extraido_dominio.domain

def analizar_historico():
    cache_dominios = cargar_cache()
    certificados = obtener_certificados_reales()
    nuevos_analizados = set()

    for dominio, certificado_simulado in certificados:
        if dominio in cache_dominios:
            logger.info(f"[ℹ️] Dominio {dominio} ya analizado, se omite.")
            continue

        if es_sospechoso(dominio):
            logger.info(f"[⚠️] Dominio sospechoso en histórico: {dominio}")
            analizar_certificado(certificado_simulado, dominio)
        else:
            logger.info(f"[ℹ️] Dominio ignorado: {dominio}")

        nuevos_analizados.add(dominio)

    # Actualizamos la cache con los nuevos dominios analizados
    cache_dominios.update(nuevos_analizados)
    guardar_cache(cache_dominios)

