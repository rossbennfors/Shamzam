import sqlite3

class Repository:
    def __init__(self,table):
        self.table = table 
        self.database = self.table + ".db" 
        self.make()

    def make(self):
        with sqlite3.connect(self.database) as connection:
            cursor = connection.cursor()
            cursor.execute(
                f"CREATE TABLE IF NOT EXISTS {self.table} " +
                "(song TEXT PRIMARY KEY, artist TEXT, full_audio BLOB)"
            )
            connection.commit()

    def clear(self):
        with sqlite3.connect(self.database) as connection:
            cursor = connection.cursor()
            cursor.execute(
                f"DELETE FROM {self.table}" 
            )
            connection.commit()

    def insert(self, js):
        with sqlite3.connect(self.database) as connection:
            cursor = connection.cursor()
            audio_data = js.get("full_audio")

            if not audio_data:
                raise ValueError("Audio data is required")

            cursor.execute(f"INSERT INTO {self.table} (song, artist, full_audio) VALUES (?, ?, ?)", 
                        (js["song"], js["artist"], audio_data))
            connection.commit()
            return cursor.rowcount


    def update(self,js):
        with sqlite3.connect(self.database) as connection:
            cursor = connection.cursor()
            cursor.execute(
                f"UPDATE {self.table} SET artist=?, full_audio=? WHERE song=?",
                (js["artist"], js["full_audio"], js["song"])
            )
            connection.commit()
            return cursor.rowcount

    def lookup(self,song):
        with sqlite3.connect(self.database) as connection:
            cursor = connection.cursor()
            cursor.execute(
                f"SELECT song, artist FROM {self.table} WHERE song=?",
                (song,)
            )
            row = cursor.fetchone()
            if row:
                return {"song":row[0],"artist":row[1]}
            else:
                return None

    def get_all_tracks(self):
        with sqlite3.connect(self.database) as connection:
            cursor = connection.cursor()
            cursor.execute(
                f"SELECT song, artist FROM {self.table}"
                )
            rows = cursor.fetchall()
            return [{"song": row[0], "artist": row[1]} for row in rows]
        
    def get_track_with_audio(self, song):
        with sqlite3.connect(self.database) as connection:
            cursor = connection.cursor()
            cursor.execute(f"SELECT song, artist, full_audio FROM {self.table} WHERE song=?", (song,))
            row = cursor.fetchone()
            if row:
                return {"song": row[0], "artist": row[1], "full_audio": row[2]}
            return None

    def delete(self, song):
        with sqlite3.connect(self.database) as connection:
            cursor = connection.cursor()
            cursor.execute(
                f"DELETE FROM {self.table} WHERE song=?", 
                (song,)
                )
            connection.commit()
            return cursor.rowcount
