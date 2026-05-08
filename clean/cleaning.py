from utils.logger import log_info, log_error
import pandas as pd
from clean.duplicates import drop_duplicates
from clean.types import validate_data_types
from clean.Missing_Values_nules import null_values

def clean_data(df):

    try :
        log_info("Starting data cleaning process")

        # --> drop duplicates
        df = drop_duplicates(df)
        # --> types
        df = validate_data_types(df)
        # --> nuul values
        df = null_values(df)


        log_info("Data cleaning process completed successfully")
        return df
    except Exception as e:
        log_error(f"Error during data cleaning: {e}")
        return None