import sqlite3


def dbCreateTables():
    conexion = sqlite3.connect("database.db")

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

    conexion.execute(
        """
        CREATE TABLE IF NOT EXISTS consult (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            reason TEXT NOT NULL,
            doctor_id INTEGER NOT NULL,
            patient_id INTEGER NOT NULL
        )
    """
    )

    conexion.execute(
        """CREATE TABLE IF NOT EXISTS patient (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            name TEXT, 
            last_name TEXT,
            dni INT,
            phone INT,
            address TEXT,
            diagnosis TEXT
            )
        """
    )

    conexion.execute(
        """CREATE TABLE IF NOT EXISTS clinicalstaff (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            name TEXT, 
            last_name TEXT,
            dni INT,
            phone INT,
            address TEXT,
            position TEXT
            )
        """
    )
