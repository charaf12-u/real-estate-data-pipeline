from utils.logger import  log_info


# --> creés price_per_m2
def add_price_features(df):
    df["price_per_m2"] = df["price"] / df["surface"]

    log_info("Created column 'price_per_m2' successfully")

    return df
