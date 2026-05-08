import pandas as pd
from utils.logger import log_info, log_error


def add_localisation_id(df, engine):
    try:
        dim = pd.read_sql("""
            SELECT id, city, district, latitude, longitude, geo_level
            FROM bi_schema.dim_localisation
        """, engine)

        df = df.merge(
            dim,
            on=["city", "district", "latitude", "longitude", "geo_level"],
            how="left"
        )

        df.rename(columns={"id": "localisation_id"}, inplace=True)

        log_info("localisation_id added")

        return df

    except Exception as e:
        log_error(f"Error adding localisation_id: {e}")
        return df


def add_caracteristiques_id(df, engine):
    try:
        dim = pd.read_sql("""
            SELECT id, bedrooms, bathrooms, floor, size_category
            FROM bi_schema.dim_caracteristiques
        """, engine)

        df = df.merge(
            dim,
            on=["bedrooms", "bathrooms", "floor", "size_category"],
            how="left"
        )

        df.rename(columns={"id": "caracteristiques_id"}, inplace=True)

        log_info("caracteristiques_id added")

        return df

    except Exception as e:
        log_error(f"Error adding caracteristiques_id: {e}")
        return df


def add_temps_id(df, engine):
    try:
        dim = pd.read_sql("""
            SELECT id, scraped_at, published_time
            FROM bi_schema.dim_temps
        """, engine)

        df = df.merge(
            dim,
            on=["scraped_at", "published_time"],
            how="left"
        )

        df.rename(columns={"id": "temps_id"}, inplace=True)

        log_info("temps_id added")

        return df

    except Exception as e:
        log_error(f"Error adding temps_id: {e}")
        return df