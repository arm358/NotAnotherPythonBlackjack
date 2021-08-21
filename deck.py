import random


class Deck:
    def __init__(self, deck_count):
        """declare a 52 card deck, then duplicate it <deck_count> number of times"""
        self.deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K", "A"] * 4
        self.create(deck_count)

    def create(self, deck_count):
        self.deck = self.deck * deck_count

    def shuffle(self):
        """randomly shuffles the created deck and returns it back"""
        random.shuffle(self.deck)
        return self.deck