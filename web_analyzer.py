from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from utils import setup_logger

logger = setup_logger()

def analyze_website(url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = None
    try:
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.set_page_load_timeout(10)
        full_url = url if url.startswith("http") else f"http://{url}"
        driver.get(full_url)
        content = driver.page_source.lower()
        keywords = ["login", "password", "bank", "verify", "account"] #puedes agregar mas keywords para mayor analisis
        score = sum(1 for kw in keywords if kw in content)
        logger.info(f"Análisis web para {url}: puntuación {score}")
        return score
    except Exception as e:
        logger.error(f"Error analizando sitio web {url}: {e}")
        return 0
    finally:
        if driver:
            driver.quit()

