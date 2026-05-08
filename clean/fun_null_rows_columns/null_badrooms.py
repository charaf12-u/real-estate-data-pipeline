from utils.logger import  log_error
from clean.fun_null_rows_columns.helpers import  create_surface_group , choose_mode


# --> bedrooms null (mode by surface , globale mode)
def handle_bedrooms_nulls(df):

    try : 
        

        if "bedrooms" not in df.columns:
            return df

        df = create_surface_group(df)

        # --> 1 : mode by surface group
        surface_group_mode = (
            df.groupby("surface_group", observed=False)["bedrooms"].agg(lambda x: choose_mode(x))
        )
        bedrooms_null_mask = df["bedrooms"].isna()

        df.loc[bedrooms_null_mask, "bedrooms"] = (
            df.loc[bedrooms_null_mask, "surface_group"].map(surface_group_mode)
        )

        # --> 2 : global mode fallback
        global_mode_bedrooms = choose_mode( df["bedrooms"] )

        df["bedrooms"] = df["bedrooms"].fillna( global_mode_bedrooms )

        df["bedrooms"] = ( df["bedrooms"].round().astype(int) )

        if "surface_group" in df.columns:
            df = df.drop(columns=["surface_group"])

        return df

    except Exception as e :
        log_error(f"erreur : {e}")
