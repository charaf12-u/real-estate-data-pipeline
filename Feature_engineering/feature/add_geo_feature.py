import pandas as pd
from utils.logger import log_info, log_error


def add_geo(df):
    try:

        geo_path = "staging/geo_coordinates.csv"
        geo_df = pd.read_csv(geo_path, encoding="utf-8-sig")

        df = df.merge(
            geo_df,
            on=["city", "district"],
            how="left"
        )

        log_info("Geo data added to dataframe")
        return df

    except Exception as e:
        log_error(f"Error adding geo: {e}")
        return df