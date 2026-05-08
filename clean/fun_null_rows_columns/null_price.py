
from clean.fun_null_rows_columns.helpers import (
    create_surface_group,
    choose_mean_or_median
)


# --> price null
# --> (district → city → surface range → bedrooms → bathrooms)

def handle_price_nulls(df):


    if "price" not in df.columns:
        return df

    df = create_surface_group(df)

    for idx in df[df["price"].isna()].index:
        row = df.loc[idx]

        # --> 1 : district
        group = df[
            (df["district"] == row["district"]) &
            (df["city"] == row["city"]) &
            (df["surface_group"] == row["surface_group"]) &
            (df["bedrooms"] == row["bedrooms"]) &
            (df["bathrooms"] == row["bathrooms"])
        ]["price"]

        fill_value = choose_mean_or_median(group)

        # --> 2 : bedrooms
        if fill_value is None:
            group = df[
                (df["district"] == row["district"]) &
                (df["city"] == row["city"]) &
                (df["surface_group"] == row["surface_group"]) &
                (df["bedrooms"] == row["bedrooms"])
            ]["price"]

            fill_value = choose_mean_or_median(group)

        # --> 3 : surface range
        if fill_value is None:
            group = df[
                (df["district"] == row["district"]) &
                (df["city"] == row["city"]) &
                (df["surface_group"] == row["surface_group"])
            ]["price"]

            fill_value = choose_mean_or_median(group)

        # --> 4 : city
        if fill_value is None:
            group = df[
                (df["city"] == row["city"]) &
                (df["surface_group"] == row["surface_group"])
            ]["price"]

            fill_value = choose_mean_or_median(group)

        # --> 5 : global fallback
        if fill_value is None:
            fill_value = choose_mean_or_median(
                df["price"]
            )

        df.at[idx, "price"] = fill_value

    if "surface_group" in df.columns:
        df = df.drop(columns=["surface_group"])

    return df