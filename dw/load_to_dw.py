from db.config.db_config import get_engine
from dw.load_dimensions import (
    load_dim_localisation,
    load_dim_caracteristiques,
    load_dim_temps
)
from dw.add_ids import (
    add_localisation_id,
    add_caracteristiques_id,
    add_temps_id
)
from dw.load_facts import load_fact, load_ml_table


def load_to_dw(df):
    engine = get_engine()

    # --> load dim
    load_dim_localisation(df, engine)
    load_dim_caracteristiques(df, engine)
    load_dim_temps(df, engine)

    # --> ids
    df = add_localisation_id(df, engine)
    df = add_caracteristiques_id(df, engine)
    df = add_temps_id(df, engine)

    # --> load fact
    load_fact(df, engine)

    # --> load ml
    load_ml_table(df, engine)

    return df