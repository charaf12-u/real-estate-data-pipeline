from clean.fun_null_rows_columns.null_city import handle_city_nulls
from clean.fun_null_rows_columns.null_distract import handle_district_nulls
from clean.fun_null_rows_columns.null_titel import handle_title_nulls
from clean.fun_null_rows_columns.null_url import handle_url_nulls
from clean.fun_null_rows_columns.null_scraped_at import handle_scraped_at_nulls
from clean.fun_null_rows_columns.published_time import handle_published_time_nulls
from clean.fun_null_rows_columns.null_surface import handle_surface_nulls
from clean.fun_null_rows_columns.null_badrooms import handle_bedrooms_nulls
from clean.fun_null_rows_columns.null_bathrooms import handle_bathrooms_nulls
from clean.fun_null_rows_columns.null_price import handle_price_nulls
from clean.fun_null_rows_columns.null_floor import handle_floor_nulls


def null_values(df):

    # --> drop columns year_built ( touts row null )
    if "year_built" in df.columns:
        df = df.drop(columns=["year_built"])

    # --> location ( city , district )
    df = handle_city_nulls(df)
    df = handle_district_nulls(df)

    # --> null titel
    df = handle_title_nulls(df)
    # --> null url
    df = handle_url_nulls(df)

    # --> time ( scraped_at , published_time )
    df = handle_scraped_at_nulls(df)
    df = handle_published_time_nulls(df)

    # --> surface , bathrooms , bedrooms , price , floor
    df = handle_surface_nulls(df)
    df = handle_bedrooms_nulls(df)
    df = handle_bathrooms_nulls(df)
    df = handle_price_nulls(df)
    df = handle_floor_nulls(df)

    return df