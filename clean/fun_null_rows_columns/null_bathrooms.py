from clean.fun_null_rows_columns.helpers import  create_surface_group, choose_mode
from utils.logger import log_error 

# --> null bathrooms ( mode bedrooms , mode surface , global mode)
def handle_bathrooms_nulls(df):
    try :
        
        if "bathrooms" not in df.columns:
            return df

        # --> 1 : bedrooms grouped mode
        if "bedrooms" in df.columns:
            bedrooms_mode = ( df.groupby("bedrooms")["bathrooms"]
                .agg(lambda x: choose_mode(x))
            )

            bathrooms_null_mask = df["bathrooms"].isna()

            df.loc[bathrooms_null_mask, "bathrooms"] = (
                df.loc[bathrooms_null_mask, "bedrooms"].map(bedrooms_mode)
            )

        # --> 2 : surface grouped mode
        df = create_surface_group(df)

        surface_group_mode = (
        df.groupby("surface_group", observed=False)["bathrooms"]
            .agg(lambda x: choose_mode(x))
        )

        bathrooms_null_mask = df["bathrooms"].isna()

        df.loc[bathrooms_null_mask, "bathrooms"] = (
            df.loc[bathrooms_null_mask, "surface_group"].map(surface_group_mode)
        )

        # --> 3 : global mode
        global_mode_bathrooms = choose_mode( df["bathrooms"] )
        df["bathrooms"] = df["bathrooms"].fillna( global_mode_bathrooms )
        df["bathrooms"] = ( df["bathrooms"].round().astype(int) )

        if "surface_group" in df.columns:
            df = df.drop(columns=["surface_group"])

        return df


    except Exception as e :
        log_error(f"erreur : {e}")