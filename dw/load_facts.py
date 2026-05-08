from utils.logger import log_info, log_error
from dw.bulk_utils import bulk_upsert


def load_fact(df, engine):
    try:
        fact = df[[
            "url", "price", "surface", "price_per_m2", "price_category", "luxury_flag",
            "rooms_density", "bathrooms_per_room", "localisation_id", "caracteristiques_id", "temps_id"
        ]]

        values = list(fact.itertuples(index=False, name=None))

        bulk_upsert(
            "bi_schema.fact_annonce",
            [
                "url", "price", "surface", "price_per_m2", "price_category", "luxury_flag",
                "rooms_density", "bathrooms_per_room","localisation_id", "caracteristiques_id", "temps_id"
            ],
            values,
            ["url"]
        )

        log_info("Fact_Annonce loaded")

    except Exception as e:
        log_error(f"Error loading fact: {e}")


def load_ml_table(df, engine):
    try:
        ml = df[[
            "url" , "price", "surface", "bedrooms", "bathrooms", "floor", "city", "district", "latitude",
            "longitude", "price_per_m2", "size_category", "price_category", "luxury_flag",
            "rooms_density", "bathrooms_per_room"
        ]]

        values = list(ml.itertuples(index=False, name=None))

        bulk_upsert(
            "ml_schema.dataset_ml",
            [
                "url" , "price", "surface", "bedrooms", "bathrooms", "floor", "city", "district", 
                "latitude", "longitude", "price_per_m2", "size_category", "price_category",
                "luxury_flag", "rooms_density", "bathrooms_per_room"
            ],
            values,
            ["url"]
        )

        log_info("ML table loaded")

    except Exception as e:
        log_error(f"Error loading ML table: {e}")