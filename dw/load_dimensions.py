import pandas as pd
from utils.logger import log_info, log_error
from dw.bulk_utils import bulk_upsert


def load_dim_localisation(df, engine):
    try:
        # --> les col
        dim = df[[ "city", "district", "latitude", "longitude", "geo_level" ]].drop_duplicates()
        # --> df to tuples ( pour insert )
        values = list(dim.itertuples(index=False, name=None))

        bulk_upsert(
            "bi_schema.dim_localisation",
            ["city", "district", "latitude", "longitude", "geo_level"],
            values,
            ["city", "district"]
        )

        log_info("Dim_Localisation loaded")

    except Exception as e:
        log_error(f"Error loading dim_localisation: {e}")


def load_dim_caracteristiques(df, engine):
    try:
        dim = df[[ "bedrooms", "bathrooms", "floor", "size_category" ]].drop_duplicates()

        values = list(dim.itertuples(index=False, name=None))

        bulk_upsert(
            "bi_schema.dim_caracteristiques", 
            ["bedrooms", "bathrooms", "floor", "size_category"],
            values, 
            ["bedrooms", "bathrooms", "floor", "size_category"]
        )

        log_info("Dim_Caracteristiques loaded")

    except Exception as e:
        log_error(f"Error loading dim_caracteristiques: {e}")


def load_dim_temps(df, engine):
    try:
        df["scraped_at"] = pd.to_datetime(df["scraped_at"], errors="coerce")
        df["published_time"] = pd.to_datetime(df["published_time"], errors="coerce")
        df["year"] = df["scraped_at"].dt.year
        df["month"] = df["scraped_at"].dt.month
        df["day"] = df["scraped_at"].dt.day

        dim = df[[ "scraped_at", "published_time", "year", "month", "day" ]].drop_duplicates()

        values = list(dim.itertuples(index=False, name=None))

        bulk_upsert(
            "bi_schema.dim_temps", ["scraped_at", "published_time", "year", "month", "day"],
            values, ["scraped_at", "published_time"]
        )

        log_info("Dim_Temps loaded")

    except Exception as e:
        log_error(f"Error loading dim_temps: {e}")