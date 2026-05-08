from pathlib import Path
import pandas as pd
from utils.logger import log_info, log_error



# --> read pop file in staging/data_scraping/
def read_latest_csv_file():
    
    try:
        
        folder_path = Path("staging/data_scraping")

        # --> check folder exists
        if not folder_path.exists():
            log_error("Folder staging/data_scraping does not exist")
            return None
        # --> get all csv files
        csv_files = list(
            folder_path.glob("*.csv")
        )

        if not csv_files:
            log_error("No CSV files found in staging/data_scraping")
            return None

        # --> get latest file by modification time
        latest_file = max( csv_files,
            key=lambda file: file.stat().st_mtime
        )

        # --> read csv
        df = pd.read_csv( latest_file , encoding="utf-8-sig" )

        log_info(f"Latest CSV file '{latest_file.name}' read successfully")


        return df

    except Exception as e:
        log_error(f"Error reading latest CSV file: {e}")
        return None