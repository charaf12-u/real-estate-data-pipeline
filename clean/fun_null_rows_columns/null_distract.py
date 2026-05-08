import pandas as pd
from utils.logger import log_error

# --> null district ( title --> url --> city grouped mode --> global mode --> drop )
def handle_district_nulls(df):

    # --> fun extract district from titel
    def extract_district_from_title(title):
        try :
            if pd.isna(title):
                return None
            title = str(title).lower()
            for district in known_districts:
                if str(district).lower() in title:
                    return district
            return None
        except Exception as e :
            log_error(f"erreur : {e}")

    # --> fun extract district from url
    def extract_district_from_url(url):
        try :
            if pd.isna(url):
                return None
            url = str(url).lower()
            for district in known_districts:
                if str(district).lower().replace(" ", "_") in url:
                    return district
            return None
        except Exception as e :
            log_error(f"erreur : {e}")



    try :

        known_districts = df["district"].dropna().unique()
        # --> distract par titel
        if "district" in df.columns and "title" in df.columns:
            district_null_mask = df["district"].isna()

            df.loc[district_null_mask, "district"] = (
                df.loc[district_null_mask, "title"]
                .apply(extract_district_from_title)
            )

        # --> distract par url
        if "url" in df.columns:
            district_null_mask = df["district"].isna()

            df.loc[district_null_mask, "district"] = (
                df.loc[district_null_mask, "url"]
                .apply(extract_district_from_url)
            )

        # --> distract par city 
        if "city" in df.columns:
            city_district_map = (
                df.dropna(subset=["city", "district"])
                .groupby("city")["district"]
                .agg(lambda x: x.mode()[0])
            )
            district_null_mask = df["district"].isna()
            df.loc[district_null_mask, "district"] = (
                df.loc[district_null_mask, "city"]
                .map(city_district_map)
            )

        # --> global mode fallback
        if df["district"].isna().sum() > 0:
            global_mode_district = df["district"].mode()[0]

            df["district"] = df["district"].fillna(global_mode_district)

        # --> drop 
        df = df.dropna(subset=["district"])

        return df


    except Exception as e :
        log_error(f"erreur : {e}")
    