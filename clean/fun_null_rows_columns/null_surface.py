
from clean.fun_null_rows_columns.helpers import  choose_mean_or_median


# --> surface null
# --> (handle by district → bedrooms → bathrooms → global fallback)

def handle_surface_nulls(df):

    if "surface" not in df.columns:
        return df

    # --> 1 : district
    if "district" in df.columns:
        for idx in df[df["surface"].isna()].index:
            row = df.loc[idx]
            group = df[ df["district"] == row["district"] ]["surface"]
            fill_value = choose_mean_or_median(group)

            if fill_value is not None:
                df.at[idx, "surface"] = fill_value

    # --> 2 : bedrooms
    if "bedrooms" in df.columns:
        for idx in df[df["surface"].isna()].index:
            row = df.loc[idx]
            group = df[df["bedrooms"] == row["bedrooms"]]["surface"]
            fill_value = choose_mean_or_median(group)

            if fill_value is not None:
                df.at[idx, "surface"] = fill_value

    # --> 3 : bathrooms
    if "bathrooms" in df.columns:
        for idx in df[df["surface"].isna()].index:
            row = df.loc[idx]
            group = df[df["bathrooms"] == row["bathrooms"]]["surface"]
            fill_value = choose_mean_or_median(group)

            if fill_value is not None:
                df.at[idx, "surface"] = fill_value

    # --> 4 : global fallback
    global_fill_value = choose_mean_or_median(df["surface"])

    if global_fill_value is not None:
        df["surface"] = df["surface"].fillna( global_fill_value )

    return df