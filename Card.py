'''Card base class'''

import uuid


class Card:
    def __init__(self, front: str, back: str, deck = None, id: int = None) -> None:
        self.front: str = front
        self.back: str = back
        self.deck = deck

        # Grab first 32 bits from uuid generated from uuid1()
        if id:
            self.id = id
        else:
            self.id = int(hash(''.join((self.front, self.back))))

    
    def __iter__(self):
        return iter(list((self.front, self.back, self.deck, self.id)))


    # def __str__(self):
    #     return 

    
    # def __repr__(self):
    #     return self.__str__()


    def get_front(self) -> str:   
        return self.front

    
    def get_back(self) -> str:
        return self.back

    
    def get_id(self) -> int:
        return self.id
