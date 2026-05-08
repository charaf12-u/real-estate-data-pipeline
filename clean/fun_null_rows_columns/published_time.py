import pandas as pd
from datetime import timedelta

# --> publication date, time between articles
# --> (max gap threshold --> validation with scraped_at --> strict drop)
def handle_published_time_nulls(df):
    
    if "published_time" not in df.columns:
        return df
    if "scraped_at" not in df.columns:
        return df

    # --> convert to datetime
    df["published_time"] = pd.to_datetime( df["published_time"], errors="coerce" )
    df["scraped_at"] = pd.to_datetime( df["scraped_at"], errors="coerce" )

    # --> max time gap between articles in days
    max_gap = timedelta(days=3)

    # --> rows with null published_time
    for idx in df[df["published_time"].isna()].index:

        prev_time = None
        next_time = None

        # --> previous valid published_time
        prev_rows = df.loc[:idx - 1, "published_time"].dropna()
        if not prev_rows.empty:
            prev_time = prev_rows.iloc[-1]

        # --> next valid published_time
        next_rows = df.loc[idx + 1:, "published_time"].dropna()
        if not next_rows.empty:
            next_time = next_rows.iloc[0]

        
        if prev_time is not None and next_time is not None:

            gap = next_time - prev_time
            if gap <= max_gap:
                midpoint = prev_time + (gap / 2)
                if midpoint <= df.loc[idx, "scraped_at"]:
                    df.loc[idx, "published_time"] = midpoint

    # --> fallback:
    missing_mask = df["published_time"].isna()
    df.loc[missing_mask, "published_time"] = ( df.loc[missing_mask, "scraped_at"] )

    # -->final validation
    invalid_mask = ( df["published_time"] > df["scraped_at"] )
    df = df[~invalid_mask]

    # --> if still null → drop
    df = df.dropna(subset=["published_time"])

    return df