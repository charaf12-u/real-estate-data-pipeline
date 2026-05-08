from selenium.webdriver.common.by import By
from utils.logger import log_info  , log_warning


# --> extract element in text
def safe_find_text(element, by, value):
    try:
        log_info(f"Successfully found text for element with {by}='{value}'")
        return element.find_element(by, value).text
        
    except:
        log_warning(f"Could not find text for element with {by}='{value}'")
        return None


# --> extract href in element (url)
def safe_find_href(element):
    try:
        log_info("Successfully found href for element")
        return element.get_attribute("href")
        
    except:
        log_warning("Could not find href for element")
        return None
    

# --> extract number (desimal)
def extract_number(text):
    if not text:
        log_warning("No text provided for number extraction")
        return None

    numbers = "".join([c for c in text if c.isdigit()])
    log_info(f"Extracted numbers: {numbers}")
    return int(numbers) if numbers else None