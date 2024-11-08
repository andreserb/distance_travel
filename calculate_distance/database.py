import sqlite3
import os
class Database:
    def __init__(self, id, name, latitude, longitude):
        self.id = id
        self.name = name
        self.latitude = latitude
        self.longitude = longitude


    def save_location(self):
        # Create the db folder if it does not exist
        db_folder = "db"
        if not os.path.exists(db_folder):
            os.makedirs(db_folder)
        # Create a new connection object with check_same_thread=False
        db_path = os.path.join(db_folder, "locations.db")
        conn = sqlite3.connect(db_path, check_same_thread=False)
        cursor = conn.cursor()
        # Create the locations table if it does not exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS locations (
                id TEXT PRIMARY KEY,
                name TEXT,
                latitude REAL,
                longitude REAL
            )
        """)
        # Insert data into the locations table
        cursor.execute("INSERT INTO locations (id, name, latitude, longitude) VALUES (?, ?, ?, ?)",
                       (self.id, self.name, self.latitude, self.longitude))
        conn.commit()
        conn.close()

    def get_location(location_id):
        """Retrieve a location by its ID."""
        database = os.path.join("db", "locations.db")
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM locations WHERE id = ?', (location_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return {"id": row[0], "name": row[1], "latitude": row[2], "longitude": row[3]}
        return None