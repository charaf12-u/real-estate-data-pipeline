from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pandas as pd
from datetime import datetime
from pathlib import Path
from utils.logger import log_info, log_error
from extract.pagination import scrape_pages


def extract():
    try:

        # --> option (configuration de seting chrome)
        chrome_options = Options()
        # --> seting ( )
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")

        # --> important in docker
        chrome_options.binary_location = "/usr/bin/chromium"

        service = Service("/usr/bin/chromedriver")
        
        # --> ouvrir browser (chrome)
        browser = webdriver.Chrome(
            service=service,
            options=chrome_options
        )
        url_site = "https://www.avito.ma/fr/maroc/appartements-à_vendre"
        browser.get(url_site)
        
        # --> resemple data
        all_data = scrape_pages(browser, total_pages=5)
        df = pd.DataFrame(all_data)

        # --> stocker le file ( staging/data_scraping/raw_avito_X.X.X.X.X.csv)
        output_folder = Path("staging/data_scraping")
        output_folder.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M")
        file_path = output_folder / f"raw_avito_{timestamp}.csv"
        df.to_csv(file_path, index=False, encoding="utf-8-sig")

        log_info("CSV file saved successfully")
        log_info(f"Total annonces collectées : {len(df)}")
        log_info(f"Saved in : {file_path}")

        browser.quit()
        return file_path

    except Exception as e:
        log_error(f"extract error: {e}")