import sqlite3
from config import booth_lst

def initialize_database():
    conn = sqlite3.connect("sdhsf2.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS reservations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            booth TEXT NOT NULL,
            order_number INTEGER NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS order_sequence (
            booth TEXT PRIMARY KEY,
            last_order_number INTEGER NOT NULL
        )
        """
    )

    for b in booth_lst:
        cursor.execute("SELECT booth FROM order_sequence WHERE booth = ?", (b,))
        exists = cursor.fetchone()

        if not exists:
            cursor.execute(
                "INSERT INTO order_sequence (booth, last_order_number) VALUES (?, 0)",
                (b,),
            )

    conn.commit()
    conn.close()

def get_database_connection():
    return sqlite3.connect("sdhsf2.db")
