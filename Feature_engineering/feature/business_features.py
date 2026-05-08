from utils.logger import log_info, log_error


def add_business_features(df):
    try:
        # --> crees category par pice
        def price_category(price_m2):
            if price_m2 < 8000:
                return "cheap"
            elif price_m2 < 15000:
                return "normal"
            else:
                return "expensive"

        df["price_category"] = df["price_per_m2"].apply(price_category)

        # --> luxury_flag
        df["luxury_flag"] = (df["price_per_m2"] > 15000).astype(int)

        # --> nomber de bedrooms par m²
        df["rooms_density"] = df["bedrooms"] / df["surface"]

        # --> nomber de bathrooms pour bedrooms
        df["bathrooms_per_room"] = df["bathrooms"] / df["bedrooms"]

        log_info("Created business features successfully")

        return df

    except Exception as e:
        log_error(f"Error in add_business_features: {e}")
        return df