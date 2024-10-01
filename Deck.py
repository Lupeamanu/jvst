'''Deck.py'''

import uuid

from Card import Card


class Deck:
    def __init__(self, name: str, tags: list[str] = None, cards: list[Card] = [], id: int = None) -> None:
        self.name: str = name
        self.tags: list[str] = tags
        self.cards: list[Card] = cards

        if id:
            self.id = id
        else:
            # Grab first 32 bits from uuid generated from uuid1()
            self.id = int(hash(self.name))

    
    def __iter__(self):
        return iter(list((self.name, self.tags, self.cards, self.id)))

    
    def __str__(self):
        data = list(self)

        return str(data)


    def __repr__(self):
        return self.__str__()

    
    def get_cards(self) -> list[Card]:
        return self.cards


    def get_id(self) -> int:
        return self.id

    
    def get_name(self) -> str:
        return self.name

    
    def view_deck(self) -> dict:
        card_dict = { card.front: card.back for card in self.cards }

        return {
            "name": self.name,
            "tags": self.tags,
            "cards": card_dict,
            "id": self.id
        }
