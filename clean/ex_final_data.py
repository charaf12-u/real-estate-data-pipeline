from pathlib import Path
from datetime import datetime
from utils.logger import log_info, log_error


# --> save data cleaned in staging/data_cleaned
def save_cleaned_data(df):
    try:

        # --> folder staging/data_cleaned/
        output_folder = Path( "staging/data_cleaned" )
        output_folder.mkdir(
            parents=True,
            exist_ok=True
        )

        # --> time file
        timestamp = datetime.now().strftime(
            "%Y_%m_%d_%H_%M"
        )
        # --> name file 
        file_name = (
            f"cleaned_avito_{timestamp}.csv"
        )
        file_path = output_folder / file_name

        # --> save folder
        df.to_csv(
            file_path,
            index=False,
            encoding="utf-8-sig"
        )

        log_info(f"Cleaned data saved successfully: {file_path}")
        return file_path

    except Exception as e:
        log_error(f"Error saving cleaned data: {e}")
        return None