""" Handles SQLite database operations for saved celestial systems """

import sqlite3
from pathlib import Path

import simulation.bodies as bodies

# Database location
DATABASE_PATH = Path(__file__).resolve().parents[2] / "data" / "celestial.db"

class Database:
    """ Handle the celestial systems database """

    def __init__(self, database_path: Path = DATABASE_PATH):
        self.database_path = database_path

        self.database_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self._create_tables()

    def _connect(self):
        """ Create a database connection """

        connection = sqlite3.connect(self.database_path)
        connection.execute("PRAGMA foreign_keys = ON")

        return connection

    def _create_tables(self):
        """ Create a new database table """

        with self._connect() as connection:

            connection.execute("""
                CREATE TABLE IF NOT EXISTS systems (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    time REAL NOT NULL
                )
            """)

            connection.execute("""
                CREATE TABLE IF NOT EXISTS bodies (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    system_id INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    mass REAL NOT NULL,
                    radius REAL NOT NULL,
                    x REAL NOT NULL,
                    y REAL NOT NULL,
                    vx REAL NOT NULL,
                    vy REAL NOT NULL,

                    FOREIGN KEY (system_id)
                        REFERENCES systems(id)
                        ON DELETE CASCADE
                )
            """)

    def save_system(self, system: bodies.CelestialSystem):
        """ Save the current state of a celestial system """

        with self._connect() as connection:

            # Save system information
            cursor = connection.execute(
                """
                INSERT INTO systems (name, time)
                VALUES (?, ?)
                """,
                (
                    system.name,
                    float(system.time)
                )
            )

            system_id = cursor.lastrowid

            # Save every body
            for body in system.bodies:

                connection.execute(
                    """
                    INSERT INTO bodies (
                        system_id,
                        name,
                        mass,
                        radius,
                        x,
                        y,
                        vx,
                        vy
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        system_id,
                        body.name,
                        float(body.mass),
                        float(body.radius),
                        float(body.pos[0]),
                        float(body.pos[1]),
                        float(body.vel[0]),
                        float(body.vel[1])
                    )
                )

        return system_id