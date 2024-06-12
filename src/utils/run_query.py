import sqlite3


# Run query's and return the result
def run_query(query, parameters=()):
    db_name = "database.db"
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        result = cursor.execute(query, parameters)
        conn.commit()
    return result
