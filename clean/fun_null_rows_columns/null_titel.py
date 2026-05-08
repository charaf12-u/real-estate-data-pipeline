import pandas as pd


# --> title null (generate title + flag)
# --> ex : Appartement 60 m² - 3 chambres - maarif - casa

def handle_title_nulls(df):

    if "title" not in df.columns:
        return df

    df["title_generated"] = False

    def generate_title(row):
        if pd.notna(row["title"]):
            return row["title"]

        surface = row.get("surface")
        bedrooms = row.get("bedrooms")
        district = row.get("district")
        city = row.get("city")

        # --> if all columns are available
        if ( pd.notna(surface) and pd.notna(bedrooms) and pd.notna(district)  and pd.notna(city) ):
            return f"Appartement {int(surface)} m² - {int(bedrooms)} chambres - {district} - {city}"

        # --> if surface and bedrooms are not available
        elif (pd.notna(bedrooms) and pd.notna(district) and pd.notna(city)):
            return f"Appartement {int(bedrooms)} chambres - {district} - {city}"

        # --> if surface is not available
        elif pd.notna(district) and pd.notna(city):
            return f"Appartement à vendre - {district} - {city}"

        # --> if district and city are not available
        elif pd.notna(city):
            return f"Appartement à vendre - {city}"

        # --> if all columns are not available
        return "Appartement à vendre"

    missing_title_mask = df["title"].isna()

    df["title"] = df.apply(generate_title, axis=1)

    df.loc[missing_title_mask, "title_generated"] = True

    return df