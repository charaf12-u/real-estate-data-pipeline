from clean.cleaning import clean_data
from clean.import_data import read_latest_csv_file
from extract.extract import extract
from clean.ex_final_data import save_cleaned_data
from Feature_engineering.feature_engineering import feature_engineering
from dw.load_to_dw import load_to_dw
from db.run_sql import run_sql_scripts
from utils.logger import log_error , log_info


try :

    extract()
    log_info("extract done")

    df = read_latest_csv_file()
    log_info("read file csv")

    df = clean_data(df)
    log_info("clean data")

    df = feature_engineering(df)
    log_info("feature")

    save_cleaned_data(df)
    log_info("save data cleanned")

    run_sql_scripts()
    log_info("run sql scripts")
    load_to_dw(df)
    log_info("load data")


except Exception as e :
    log_error(f"Crash in pipeline: {e}")

