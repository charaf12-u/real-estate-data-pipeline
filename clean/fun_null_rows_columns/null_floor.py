import pandas as pd
from utils.logger import log_error

# --> missing = -1 (Unknown floor)
def handle_floor_nulls(df):
    
    try :

        if "floor" not in df.columns:
            return df

        df["floor"] = pd.to_numeric( df["floor"], errors="coerce" )

        # --> remplace null par -1
        df["floor"] = df["floor"].fillna(-1)
        df["floor"] = df["floor"].astype(int)

        return df

    except Exception as e :
        log_error(f"erreur : {e}")