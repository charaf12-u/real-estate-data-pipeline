import pandas as pd
from utils.logger import log_error 

# --> null city ( title --> url --> district grouped mode --> global mode --> drop )
def handle_city_nulls(df):

    # --> fun extract city from titel
    def extract_city_from_title(title):
        try :
            if pd.isna(title):
                return None
            title = str(title).lower()
            for city in known_cities:
                if str(city).lower() in title:
                    return city
            return None
        except Exception as e :
            log_error(f"erreur : {e}")

    # --> fun extract city from url
    def extract_city_from_url(url):
        try : 
            if pd.isna(url):
                return None
            url = str(url).lower()
            for city in known_cities:
                if str(city).lower().replace(" ", "_") in url:
                    return city
            return None
        except Exception as e :
            log_error(f"erreur : {e}")
    
    try : 

        known_cities = df["city"].dropna().unique()

        # --> 1 : city par titel
        if "city" in df.columns and "title" in df.columns:
            city_null_mask = df["city"].isna()

            df.loc[city_null_mask, "city"] = (
                df.loc[city_null_mask, "title"]
                .apply(extract_city_from_title)
            )

        # --> 2 : city in url
        if "url" in df.columns:
            city_null_mask = df["city"].isna()
            df.loc[city_null_mask, "city"] = (
                df.loc[city_null_mask, "url"]
                .apply(extract_city_from_url)
            )

        # --> 3 : city par group district ( mode )
        if "district" in df.columns:
            district_city_map = (
                df.dropna(subset=["district", "city"]).groupby("district")["city"].agg(lambda x: x.mode()[0])
            )
            city_null_mask = df["city"].isna()
            df.loc[city_null_mask, "city"] = (
                df.loc[city_null_mask, "district"].map(district_city_map)
              )

        # --> 4 : global mode fallback
        if df["city"].isna().sum() > 0:
            global_mode_city = df["city"].mode()[0]
            df["city"] = df["city"].fillna(global_mode_city)

        # --> drop null
        df = df.dropna(subset=["city"])

        return df



    except Exception as e :
        log_error(f"error : {e}")