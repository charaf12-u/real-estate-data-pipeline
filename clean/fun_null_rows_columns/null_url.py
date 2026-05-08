# file: fill_url.py

import pandas as pd


# --> url null
# -->(recover probable exact match --> if not found → drop row )

def handle_url_nulls(df):


    if "url" not in df.columns:
        return df

    df["url_generated"] = False

    reference_rows = df[df["url"].notna()].copy()
    missing_url_rows = df[df["url"].isna()].copy()

    for idx, row in missing_url_rows.iterrows():
        candidates = reference_rows.copy()

        # --> if same city
        if pd.notna(row["city"]):
            candidates = candidates[ candidates["city"] == row["city"] ]

        # --> if same district
        if pd.notna(row["district"]):
            candidates = candidates[ candidates["district"] == row["district"] ]

        # --> if same price
        if pd.notna(row["price"]):
            candidates = candidates[ candidates["price"] == row["price"] ]

        # --> if same surface
        if pd.notna(row["surface"]):
            candidates = candidates[ candidates["surface"] == row["surface"] ]

        # --> if same bedrooms
        if pd.notna(row["bedrooms"]):
            candidates = candidates[ candidates["bedrooms"] == row["bedrooms"] ]

        # --> if only one exact probable match
        if len(candidates) == 1:
            recovered_url = candidates.iloc[0]["url"]

            df.loc[idx, "url"] = recovered_url
            df.loc[idx, "url_generated"] = True

    # --> if url still null → drop row
    df = df.dropna(subset=["url"])

    return df