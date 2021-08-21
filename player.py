class Player:
    def __init__(self, name, dealer=False, credits=10):
        self.name = name
        self.dealer = dealer
        self.cards = []
        self.bust = False
        self.blackjack = False
        self.credits = credits
        self.bet = 0
        self.bet_flag = False
        self.stay = False
        self.push = False
        self.winner = False
        self.payout = 0

    def reset(self):
        """
        return class variables to defaults. This is called after a hand is played
        and does not change name, dealer flag, or current credits amount.
        """
        self.cards = []
        self.bust = False
        self.blackjack = False
        self.bet = 0
        self.bet_flag = False
        self.stay = False
        self.push = False
        self.winner = False
        self.payout = 0

    def card_total(self):
        """
        Calculate the current hand's total. This also accounts for Aces being
        either a 1 or 11. Will return both options if both <= 21, and only return
        the lowest value if one value > 21.
        """
        total = []
        total2 = []
        for card in self.cards:
            if type(card) is int:
                total.append(card)
                total2.append(card)
                continue
            elif card != "A":
                total.append(10)
                total2.append(10)
                continue
            else:
                total.append(11)
                total2.append(1)

        self.total = sum(total)
        self.total2 = sum(total2)

        if self.total == self.total2:
            return [self.total]
        elif self.total > 21 and self.total2 < 22:
            return [self.total2]
        elif self.total2 > 21 and self.total < 22:
            return [self.total]
        elif self.total2 > 21 and self.total > 21:
            return [min(self.total, self.total2)]
        else:
            return [self.total, self.total2]