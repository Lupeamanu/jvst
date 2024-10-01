"""Script to run tool"""

# Script uses a local DB named 'jvlt.db'
import ast
import sqlite3

# Third party
from Card import Card
from Deck import Deck
from DatabaseDriver import Driver

# Initialize db driver
# Will create tables if non-existant
DB_DRIVER: Driver = Driver("jvlt.db")


def initialize_decks() -> list[Deck]:
    # Initialize decks and cards
    db_decks: list[tuple] = get_decks()
    print(db_decks)
    decks: list[Deck] = []
    for deck in db_decks:
        name = deck[0]
        tags = ast.literal_eval(deck[1])
        cards = ast.literal_eval(deck[2])
        deck_id = deck[3]
        
        decks.append(Deck(name=name, tags=tags, cards=cards, id=deck_id))

    return decks


def initialize_cards() -> list[Card]:
    db_cards: list[tuple] = get_cards()
    cards: list[Card] = []

    for card in db_cards:
        front = card[0],
        back = card[1],
        deck = card[2],
        card_id = card[3]

        new_card = Card(front=front, back=back, deck=deck, id=card_id)

        cards.append(new_card)

    return cards


def get_decks() -> list[tuple]:
    decks = DB_DRIVER.execute("select * from decks")

    return decks.fetchall()


def get_cards() -> list[tuple]:
    cards = DB_DRIVER.execute("select * from cards")

    return cards.fetchall()


def create_card(decks: list[Deck]) -> Card:
    # Get user input
    front: str = str(input("###  Enter front of card\n"))
    back: str = str(input("\n###  Enter back of card \n"))
    deck_check: str = str(input("\n###  Add card to a deck? (y/n)\n"))

    deck_selection: int = 0
    if deck_check == 'y':

        for idx, deck in enumerate(decks):
            print(f"{idx+1}: {deck.get_name()}")

        deck_selection = int(input("Select a deck: ")) - 1

        card = Card(front=front, back=back, deck=decks[deck_selection].get_id())

        # Append card to deck
        for deck in decks:
            print(deck)
            if deck.id == card.deck:
                print(vars(deck))
                deck.get_cards().append(card)

        DB_DRIVER.insert_obj(card)
        DB_DRIVER.execute(f"UPDATE DECKS set cards = {deck.get_cards()} WHERE id = {deck.get_id()}")
        DB_DRIVER.commit()

        print(f"###  Card created and added to deck with id: {decks[deck_selection].get_id()}")

    else: 
        card = Card(front=front, back=back)

        DB_DRIVER.insert_obj(card)
        DB_DRIVER.commit()

        print("### Card created!")


def create_deck() -> Deck:
    name: str = str(input("### Name the deck\n"))

    deck = Deck(name)

    # Add to db
    DB_DRIVER.insert_obj(deck)


def parse_cards(cards: list[Card], decks: list[Deck]) -> None:
    """Parses our initialized list of cards and appends cards to appropriate decks via Deck ID.

    Args:
        cards (list[Card]): Initialized list of cards to be parsed.
        decks (list[Deck]): Initialized list of decks to append any necessary cards to.
    """
    for card in cards:
        print(f"Parsing card: {card}")
        for deck in decks:
            print(f"Checking deck: {deck.name}")
            print(card.deck, deck.id)
            if card.deck == deck.id:
                print(f"Got hit: {card.front}, {deck.name}")
                deck.get_cards().append(card)
                DB_DRIVER.execute(f"UPDATE DECKS set cards = {deck.get_cards()} WHERE id = {deck.get_id()}")
            else:
                pass
    
    DB_DRIVER.commit()


if __name__ == "__main__":
    
    # Initialize decks
    decks: list[Deck] = initialize_decks()
    print(decks)

    # Initialize cards
    cards: list[Card] = initialize_cards()

    # Once we have decks, we can initialize cards
    # Using the mapping of Deck ID in the card
    # object, we can append cards to the list of
    # cards within each Deck object

    # print(cards)

    # parse_cards(cards=cards, decks=decks)

    # create_deck()
    create_card(decks=decks)

    # DB_DRIVER.execute('drop table cards')
    # DB_DRIVER.execute('drop table decks')