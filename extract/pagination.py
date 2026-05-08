from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor
from extract.scraper import scrape_listing
from utils.logger import log_info, log_error


def scrape_pages(browser, total_pages=5):
    all_data = []
    seen_urls = set()

    for page in range(1, total_pages + 1):
        try:
            log_info(f"Scraping page {page}")

            # url par les page
            if page == 1:
                page_url = "https://www.avito.ma/fr/maroc/appartements-%C3%A0_vendre"
            else:
                page_url = f"https://www.avito.ma/fr/maroc/appartements-%C3%A0_vendre?o={page}"

            browser.get(page_url)
            log_info(browser.current_url)

            # --> apres 10s pour afficher tout les card (timeout == 10s)
            WebDriverWait(browser, 10).until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, '.listing > a')
                )
            )
            # --> extrer tout cards 
            cards = browser.find_elements(
                By.CSS_SELECTOR,
                ".listing > a"
            )
            log_info(f"Cards found: {len(cards)}")

            # --> applique Threads sur 10 cards max
            with ThreadPoolExecutor(max_workers=10) as executor:
                # --> applique scrape_listing pour les cards
                results = list(executor.map(scrape_listing, cards))
            # --> remplir data
            for data in results:
                if data and data["url"] not in seen_urls:
                    seen_urls.add(data["url"])
                    all_data.append(data)

        except Exception as e:
            log_error(f"Erreur page {page}: {e}")

    return all_data