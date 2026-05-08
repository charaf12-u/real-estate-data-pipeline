import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db.config.db_config import get_engine
from utils.logger import log_info , log_error
from sqlalchemy import text



def run_sql_scripts():
    try :

        # --> run SQL (tables, indexes, views)
        log_info("Initializing SQL Database Schema...")
        engine = get_engine()
        sql_files = [
            "sql/01_create_schema.sql",
            "sql/02_create_dim_tables.sql",
            "sql/03_create_fact_table.sql",
            "sql/04_create_ml_table.sql",
            "sql/05_indexes.sql"
        ]
        # --> execute SQL scripts
        with engine.begin() as conn:
            for sql_file in sql_files:
                file_path = os.path.abspath(
                    os.path.join(os.path.dirname(__file__), '..', 'db', sql_file)
                )
                if os.path.exists(file_path):
                    log_info(f"Executing {sql_file}...")
                    with open(file_path, "r", encoding="utf-8") as f:
                        sql_query = f.read()
                    try:
                        conn.execute(text(sql_query))
                    except Exception as e:
                        log_error(str(e))
                else:
                    log_error(f"File not found: {file_path}")

    except Exception as e :
        log_error(f"erreur : {e}")