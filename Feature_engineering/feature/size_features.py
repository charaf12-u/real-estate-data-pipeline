from utils.logger import log_info, log_error


def add_size_features(df):
    try:
        def size_category(surface):
            if surface < 60:
                return "small"
            elif surface < 120:
                return "medium"
            else:
                return "large"

        df["size_category"] = df["surface"].apply(size_category)

        log_info("Created column 'size_category' successfully")

        return df

    except Exception as e:
        log_error(f"Error in add_size_features: {e}")
        return df