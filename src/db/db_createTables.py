import sqlite3


def dbCreateTables():
    conexion = sqlite3.connect("database.db")
    conexion.execute(
        """CREATE TABLE IF NOT EXISTS product (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, price REAL)"""
    )

    conexion.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """
    )
