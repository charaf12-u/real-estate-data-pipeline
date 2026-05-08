from utils.logger import log_info, log_error

# --> drop duplicates par url
def drop_duplicates(df):
    
    if "url" in df.columns:
        before = df.shape[0]
        df = df.drop_duplicates(subset=["url"])
        after = df.shape[0]
        log_info(f"Removed {before - after} duplicates based on URL.")

    else:
        log_error("Column 'url' not found in DataFrame.")
    return df