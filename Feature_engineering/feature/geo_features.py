import pandas as pd
from geopy.geocoders import Nominatim
from utils.logger import log_info, log_error
from time import sleep
import os


# --> RETRY WITH BACKOFF ( par defaut = 3fois )
def geocode_with_retry(geolocator, query, retries=3):
    for i in range(retries):
        try:
            location = geolocator.geocode(query)
            if location:
                return location
        except Exception as e:
            wait = (i + 1) * 3  # --> (3s -> 6s -> 9s
            log_error(f"Retry {i+1} → sleeping {wait}s ({query})")
            sleep(wait)

    return None


# --> 
def build_geo_cache(df):
    try:
        # --> data && cache path
        df_geo = df[["city", "district"]].dropna().drop_duplicates()
        cache_path = "staging/geo_coordinates.csv"

        # --> if deja trouve cache_path
        if os.path.exists(cache_path):
            df_cache = pd.read_csv(cache_path, encoding="utf-8-sig")
            log_info("Geo cache loaded")
            # --> new data + cache
            df_geo = df_geo.merge(
                df_cache[["city", "district"]],
                on=["city", "district"],
                how="left",
                indicator=True
            )
            # --> new data only
            df_geo = df_geo[df_geo["_merge"] == "left_only"].drop(columns=["_merge"])

        else:
            df_cache = pd.DataFrame(
                columns=["city", "district", "latitude", "longitude", "geo_level"]
            )

        # --> not data
        if df_geo.empty:
            log_info("No new geo data to process")
            return

        # --> api geopy
        geolocator = Nominatim(user_agent="avito_geo", timeout=5)

        results = []

        # --> data row par row
        for _, row in df_geo.iterrows():
            try:
                # --> lat , lon --> par district && city
                geo_level = "district"
                query = f"{row['district']} {row['city']} Morocco"
                location = geocode_with_retry(geolocator, query)
                # --> lat , lon --> par city
                if not location:
                    query = f"{row['city']} Morocco"
                    location = geocode_with_retry(geolocator, query)
                    geo_level = "city"
                # --> lat , lon 
                if location:
                    lat, lon = location.latitude, location.longitude
                    log_info(f"[OK] {query}")
                else:
                    lat, lon = None, None
                    geo_level = "unknown"
                    log_error(f"[ERREUR] {row['district']} - {row['city']}")

                results.append({
                    "city": row["city"],
                    "district": row["district"],
                    "latitude": lat,
                    "longitude": lon,
                    "geo_level": geo_level
                })

                sleep(2)

            except Exception as e:
                log_error(f"Geo error: {e}")

                results.append({
                    "city": row["city"],
                    "district": row["district"],
                    "latitude": None,
                    "longitude": None,
                    "geo_level": "unknown"
                })

        # --> new df
        df_new = pd.DataFrame(results)
        # --> df final
        if df_cache.empty:
            df_final = df_new
        else:
            df_final = pd.concat([df_cache, df_new], ignore_index=True)

        # --> clean final et export csv
        df_final = df_final.drop_duplicates(subset=["city", "district"])
        df_final.to_csv(cache_path, index=False, encoding="utf-8-sig")

        log_info("Geo cache updated successfully")

    except Exception as e:
        log_error(f"Global geo error: {e}")