import pandas as pd
from utils.logger import log_info , log_error


# --> creat surface_group column
def create_surface_group(df):
    
    try :

        if "surface" not in df.columns:
            df["surface_group"] = None
            return df

        df["surface_group"] = pd.cut(
            df["surface"],
            bins=[0, 60, 100, 150, 300, 1000],
            labels=[
                "0-60",
                "60-100",
                "100-150",
                "150-300",
                "300+"
            ]
        )
        log_info(" add columns surface_group sassufll")
        return df

    except Exception as e :
        log_error(f"erreur : {e}")

# --> choose mean or median using skewness ( 0.5 )
def choose_mean_or_median(series, min_sample_size=5):
    
    try :

        series = series.dropna()

        if len(series) < min_sample_size:
            return None
    
        # --> calcule skewness
        skewness = series.skew()
        # --> appliqui mean pour skewness < 0.5
        if abs(skewness) < 0.5:
            return series.mean()
        # --> appliqui median pour skewness > 0.5
        return series.median()

    except Exception as e :
        log_error(f"erreur : {e}")

# --> choose mode 
def choose_mode(series):
    
    try :
        series = series.dropna()

        if series.empty:
            return None

        mode_values = series.mode()

        if mode_values.empty:
            return None

        return mode_values.iloc[0]
    
    except Exception as e :
        log_error(f"erreur : {e}")