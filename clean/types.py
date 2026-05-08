from datetime import  timedelta
import pandas as pd


def convert_published_time(value, reference_time):
    # --> return pd.NaT par valeur null
    if pd.isna(value):
        return pd.NaT

    # --> tawehid text
    value = str(value).lower()

    # --> returen time par ( min , h , j , hier , aujourd)
    if "minute" in value:
        number = int("".join(filter(str.isdigit, value)))
        return reference_time - timedelta(minutes=number)
    elif "heure" in value:
        number = int("".join(filter(str.isdigit, value)))
        return reference_time - timedelta(hours=number)
    elif "jour" in value:
        number = int("".join(filter(str.isdigit, value)))
        return reference_time - timedelta(days=number)
    elif "hier" in value:
        return reference_time - timedelta(days=1)
    elif "aujourd" in value:
        return reference_time
    return pd.NaT

# --> validation type
def validate_data_types(df):

    df_string_columns = ["title", "city", "district", "url"]
    df_numeric_columns = ["price"]
    numeric_columns = ["surface", "bedrooms", "bathrooms", "floor"]

    # --> column str --> numeric
    for col in numeric_columns:
        if col in df.columns:
            df[col] = df[col].astype(str).str.extract(r"(\d+)")
            df[col] = df[col].astype(float)
        else:
            print(f"Column '{col}' not found")

    # --> column str
    for col in df_string_columns:
        if col in df.columns:
            df[col] = df[col].astype("string")
        else:
            print(f"Warning: Column '{col}' not found in DataFrame.")

    # --> columns numeric
    for col in df_numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
        else:
            print(f"Warning: Column '{col}' not found in DataFrame.")

    # --> convert le time exact pour published la annance
    if "published_time" in df.columns and "scraped_at" in df.columns:
        df["scraped_at"] = pd.to_datetime(df["scraped_at"])
        df["published_time"] = df.apply(
            lambda row: convert_published_time(
                row["published_time"],
                row["scraped_at"]
            ),
            axis=1
        )
    else:
        print("Warning: Column 'published_time' or 'scraped_at' not found")

    return df