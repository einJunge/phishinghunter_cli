from certstream_handler import run_certstream_monitor
from config import TARGET_DOMAIN, DEMO_MODE
from utils import setup_logger
import os
import logging

logger = setup_logger()

def banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\033[1;32m" + "═" * 64)
    print("🛡️  PhishingHunter - Monitor de Certificados SSL en Tiempo Real")
    print("═" * 64 + "\033[0m")
    print(f"\033[1;36m🎯 Dominio objetivo:\033[0m {TARGET_DOMAIN}")
    print(f"\033[1;35m🔧 Modo Demo:\033[0m {'Activado (Histórico + Tiempo real)' if DEMO_MODE else 'Desactivado (Solo Tiempo real)'}")
    print("\033[1;33m⌛ Esperando coincidencias de certificados...\033[0m\n")

if __name__ == "__main__":
    banner()

    if DEMO_MODE:
        try:
            # Importa y ejecuta el análisis histórico primero
            from historical_search import analizar_historico
            logger.info("Ejecutando análisis histórico (modo demo)...")
            analizar_historico()
        except Exception as e:
            logger.error(f"Error durante el análisis histórico: {e}")

    try:
        run_certstream_monitor()
    except KeyboardInterrupt:
        print("\n\033[91m[✋] Monitor detenido por el usuario.\033[0m")
    except Exception as e:
        logger.error(f"Error inesperado: {e}")

