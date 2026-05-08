from selenium.webdriver.common.by import By
from extract.extract_utils import safe_find_text, extract_number
from utils.logger import log_info , log_error , log_warning
from datetime import datetime


# --> fun scrape card
def scrape_listing(card):
    try:
        # --> time scrape
        reference_time = datetime.now()
        # --> des info (titel , price )
        title = safe_find_text(card, By.CLASS_NAME, "iHApav")
        raw_price = safe_find_text(card, By.CLASS_NAME, "PuYkS")
        price = extract_number(raw_price)
        log_info(f"Scraping annonce : {title} - {price} MAD")
        # --> scrape url
        url = None
        try:
            url = card.get_attribute("href")
            log_info(f"URL trouvée pour l'annonce : {title} - {url}")
        except:
            log_error(f"URL non trouvée pour l'annonce : {title}")
            pass
        # --> remove ads annonce
        if url and "immoneuf" in url:
            log_info(f"Annonce ignorée (immoneuf) : {title}")
            return None

        # --> location (city , district)
        location = safe_find_text(
            card,
            By.XPATH,
            './/p[contains(text(),"Appartements dans")]'
        )
        log_info(f"Localisation trouvée pour l'annonce : {title}")

        city = None
        district = None

        if location:
            parts = location.replace(
                "Appartements dans",
                ""
            ).split(",")

            city = parts[0].strip() if len(parts) > 0 else None
            district = parts[1].strip() if len(parts) > 1 else None
            log_info(f"Ville : {city}, Quartier : {district} pour l'annonce : {title}")

        # --> published_time
        published_time = safe_find_text(
            card,
            By.XPATH,
            './/p[contains(text(),"il y a") or contains(text(),"aujourd")]' 
        )
        log_info(f"Date de publication trouvée pour l'annonce : {title}")
        # --> surface 
        surface = safe_find_text(
            card,
            By.XPATH,
            './/span[@title="Surface totale"]'
        )
        log_info(f"Surface trouvée pour l'annonce : {title}")
        # --> bedrooms
        bedrooms = safe_find_text(
            card,
            By.XPATH,
            './/span[@title="Chambres"]',
        )
        log_info(f"Nombre de chambres trouvé pour l'annonce : {title}")
        # --> bathrooms
        bathrooms = safe_find_text(
            card,
            By.XPATH,
            './/span[@title="Salle de bain"]'
        )
        log_info(f"Nombre de salles de bain trouvé pour l'annonce : {title}")
        # --> floor
        floor = safe_find_text(
            card,
            By.XPATH,
            './/span[@title="Étage"]'
        )
        log_info(f"Étage trouvé pour l'annonce : {title}")
        # --> not info in year_built !!!!!!!!
        year_built = None

        if not title or not price:
            log_warning("Annonce suspecte détectée : title ou price manquant")

        annonce_data = {
            "scraped_at": reference_time,
            "title": title,
            "price": price,
            "city": city,
            "district": district,
            "surface": surface,
            "bedrooms": bedrooms,
            "bathrooms": bathrooms,
            "floor": floor,
            "year_built": year_built,
            "published_time": published_time,
            "url": url
        }

        log_info(f"Annonce extraite : {title}")
        return annonce_data

    except Exception as e:
        log_error(f"Erreur scraping annonce : {e}")
        return None

