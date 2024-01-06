# lib/dog.py
import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    def __init__(self, name=None, breed=None, id=None):
        self.id = id
        self.name = name
        self.breed = breed

    @classmethod
    def create_table(cls):
        with CONN:
            CURSOR.execute("""
                CREATE TABLE IF NOT EXISTS dogs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    breed TEXT NOT NULL
                )
            """)

    @classmethod
    def drop_table(cls):
        with CONN:
            CURSOR.execute("DROP TABLE IF EXISTS dogs")

    def save(self):
        with CONN:
            if self.id is None:
                # Insert new record
                CURSOR.execute("INSERT INTO dogs (name, breed) VALUES (?, ?)", (self.name, self.breed))
                self.id = CURSOR.lastrowid
            else:
                # Update existing record
                CURSOR.execute("UPDATE dogs SET name=?, breed=? WHERE id=?", (self.name, self.breed, self.id))

    @classmethod
    def create(cls, name, breed):
        dog = cls(name=name, breed=breed)
        dog.save()
        return dog

    @classmethod
    def new_from_db(cls, data):
        return cls(id=data[0], name=data[1], breed=data[2])

    @classmethod
    def get_all(cls):
        with CONN:
            CURSOR.execute("SELECT * FROM dogs")
            return [cls(*row) for row in CURSOR.fetchall()]

    @classmethod
    def find_by_name(cls, name):
        with CONN:
            CURSOR.execute("SELECT * FROM dogs WHERE name=?", (name,))
            data = CURSOR.fetchone()
            return cls(*data) if data else None

    @classmethod
    def find_by_id(cls, dog_id):
        with CONN:
            CURSOR.execute("SELECT * FROM dogs WHERE id=?", (dog_id,))
            data = CURSOR.fetchone()
            return cls(*data) if data else None

    @classmethod
    def find_or_create_by(cls, name, breed):
        existing_dog = cls.find_by_name(name)
        if existing_dog:
            return existing_dog
        else:
            new_dog = cls.create(name, breed)
            return new_dog

    def update(self):
        with CONN:
            CURSOR.execute("UPDATE dogs SET name=? WHERE id=?", (self.name, self.id))