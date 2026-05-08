import pandas as pd
from datetime import timedelta


# --> scraped_at null (midpoint(prev , , next) + max gap threshold + strict drop)

def handle_scraped_at_nulls(df):


    if "scraped_at" not in df.columns:
        return df

    # --> convert scraped_at to datetime
    df["scraped_at"] = pd.to_datetime( df["scraped_at"], errors="coerce" )

    # --> max allowed gap threshold
    max_gap = timedelta(minutes=30)

    # --> loop through rows with null scraped_at
    for idx in df[df["scraped_at"].isna()].index:

        prev_time = None
        next_time = None

        # --> previous valid time
        prev_rows = df.loc[:idx - 1, "scraped_at"].dropna()
        if not prev_rows.empty:
            prev_time = prev_rows.iloc[-1]

        # --> next valid time
        next_rows = df.loc[idx + 1:, "scraped_at"].dropna()
        if not next_rows.empty:
            next_time = next_rows.iloc[0]

        # --> only if previous + next are available
        if prev_time is not None and next_time is not None:

            gap = next_time - prev_time

            # --> if gap is small → midpoint
            if gap <= max_gap:
                midpoint = prev_time + (gap / 2)
                df.loc[idx, "scraped_at"] = midpoint

    # --> if still null → drop row
    df = df.dropna(subset=["scraped_at"])

    return df