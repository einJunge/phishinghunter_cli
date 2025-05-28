import json
import os
import time
import requests
from config import VIRUSTOTAL_API_KEY
from utils import setup_logger

logger = setup_logger()

CACHE_FILE = "cache/vt_domain.json"
CACHE_EXPIRY = 3600  # 1 hora

def cargar_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    return {}

def guardar_cache(cache):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f)

_vt_cache = cargar_cache()

def check_domain_virustotal(domain):
    ahora = time.time()
    if domain in _vt_cache:
        cached_time = _vt_cache[domain]["timestamp"]
        if ahora - cached_time < CACHE_EXPIRY:
            logger.info(f"VT cache hit para {domain}")
            return _vt_cache[domain]["malicious"]

    url = f"https://www.virustotal.com/api/v3/domains/{domain}"
    headers = {"x-apikey": VIRUSTOTAL_API_KEY}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            malicious = data["data"]["attributes"]["last_analysis_stats"].get("malicious", 0)
            logger.info(f"VT: {domain} maliciosos detectados: {malicious}")
            _vt_cache[domain] = {"malicious": malicious, "timestamp": ahora}
            guardar_cache(_vt_cache)
            return malicious
        else:
            logger.warning(f"VT API responded with status {response.status_code} for domain {domain}")
            return 0
    except Exception as e:
        logger.error(f"Error consultando VirusTotal para {domain}: {e}")
        return 0

