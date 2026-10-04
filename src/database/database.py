""" Handles SQLite database operations for saved celestial systems """

import sqlite3
from pathlib import Path
import numpy as np

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

    def get_systems(self):
        """ Return all saved systems """

        with self._connect() as connection:

            cursor = connection.execute(
                """
                SELECT id, name, time
                FROM systems
                ORDER BY id
                """
            )

            return cursor.fetchall()

    def load_system(self, system_id):
        """ Load a system and all of its bodies """

        with self._connect() as connection:

            system_data = connection.execute(
                """
                SELECT name, time
                FROM systems
                WHERE id = ?
                """,
                (system_id,)
            ).fetchone()

            if system_data is None:
                return None

            system_name, time = system_data

            body_data = connection.execute(
                """
                SELECT name, mass, radius, x, y, vx, vy
                FROM bodies
                WHERE system_id = ?
                ORDER BY id
                """,
                (system_id,)
            ).fetchall()

        loaded_bodies = []

        for (
            name,
            mass,
            radius,
            x,
            y,
            vx,
            vy
        ) in body_data:

            pos = np.array(
                [x, y],
                dtype=np.float64
            )

            vel = np.array(
                [vx, vy],
                dtype=np.float64
            )

            loaded_bodies.append(
                bodies.CelestialBody(
                    name=name,
                    mass=mass,
                    radius=radius,
                    pos=pos,
                    vel=vel
                )
            )

        return bodies.CelestialSystem(
            name=system_name,
            bodies=loaded_bodies,
            time=np.float64(time)
        )