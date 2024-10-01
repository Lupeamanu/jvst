'''DatabaseDriver.py'''

import sqlite3
from sqlite3 import Cursor

from Deck import Deck
from Card import Card


class Driver:
    def __init__(self, db: str) -> None:
        self.conn = sqlite3.connect(db)
        self.cursor = self.conn.cursor()

        # Initialize tables if not created
        table_queries = [
            "CREATE TABLE IF NOT EXISTS cards (front text, back text, deck int, id int)",
            "CREATE TABLE IF NOT EXISTS decks (name text, tags blob, cards blob, id int)"
        ]
        for query in table_queries:
            self.execute(query)
        
        # Save changes
        self.commit()

    
    def insert_obj(self, obj: Card | Deck) -> Cursor:
        query: str = ""
        table: str = ""

        if isinstance(obj, Card):
            table = "cards"
        else:
            table = "decks"

        # Stringify items in the object to append to query
        stringify: list[str] = [f"'{str(item)}'" for item in list(obj)]

        values = f"({', '.join(stringify)})"
        query = f"INSERT INTO {table} VALUES {values}"

        self.execute(query=query)
        self.commit()

    
    def execute(self, query: str, commit: bool = False) -> Cursor:
        return self.cursor.execute(query)

    
    def commit(self) -> None:
        self.conn.commit()
