from psycopg2.extras import execute_values
from utils.logger import log_info, log_error
from db.config.db_config import get_psycopg_connection


def bulk_upsert(table, columns, values, conflict_cols):
    try:
        if not values:
            return

        conn = get_psycopg_connection()
        cursor = conn.cursor()

        cols = ", ".join(columns)
        conflict = ", ".join(conflict_cols)

        update_cols = ", ".join([
            f"{col}=EXCLUDED.{col}"
            for col in columns if col not in conflict_cols
        ])

        
        if update_cols:
            query = f"""
            INSERT INTO {table} ({cols})
            VALUES %s
            ON CONFLICT ({conflict})
            DO UPDATE SET {update_cols};
            """
        else:
            query = f"""
            INSERT INTO {table} ({cols})
            VALUES %s
            ON CONFLICT ({conflict})
            DO NOTHING;
            """

        execute_values(cursor, query, values)

        conn.commit()
        cursor.close()
        conn.close()

        log_info(f"{table} upserted successfully")

    except Exception as e:
        log_error(f"Bulk upsert error ({table}): {e}")