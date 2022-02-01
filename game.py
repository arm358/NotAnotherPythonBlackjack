import time
import json


class Game:
    def __init__(self, players, deck):
        self.players = players
        self.deck = deck

    def deal(self):
        """
        Deal 2 cards to each player that has placed a bet or if they are the dealer,
        """
        for i in range(0, 2):
            for player in self.players:
                if player.bet_flag or player.dealer:
                    player.cards.append(self.deck[0])
                    self.deck.pop(0)

    def check(self, total):
        """
        Check if the total cards are > 21 (bust) or == 21 (blackjack).
        """
        if all(i > 21 for i in total):
            print("Bust, sorry!")
            return "bust"
        if any(i == 21 for i in total):
            print("Blackjack!")
            return "blackjack"
        else:
            return False

    def hit_or_stay(self):
        """
        Main function that handles hitting (taking a card) or staying (keeping current cards).
        Also checks whether blackjack is achieved and automatically stays, or if busted automatically
        continues to the next player.
        """
        for player in self.players:
            if not player.dealer and player.bet_flag == True:
                accepted = False
                print(f"------------------------------------")
                print(f"{player.name}")
                print(f"Cards: {player.cards} | Current total: {player.card_total()}")
                while not player.stay:
                    check = self.check(player.card_total())
                    if check == False:  # if not busted or blackjack
                        print(f"Hit or Stay?")
                        while not accepted:
                            action = input().lower()
                            if action not in ["hit", "stay"]:  # only two options allowed
                                print("Please enter hit or stay.")
                            else:
                                accepted = True
                            if action == "hit":  # append current players cards with top card of deck and delete top card
                                player.cards.append(self.deck[0])
                                self.deck.pop(0)
                                print(f"Cards: {player.cards} | Current total: {player.card_total()}")
                            if action == "stay":  # keep current cards and move to next player
                                print(f"{player.name} stays.")
                                player.stay = True
                                continue

                    else:  # either busted or blackjack achieved
                        if check == "blackjack":
                            player.stay = True
                            player.blackjack = True
                            continue
                        elif check == "bust":
                            player.stay = True
                            player.bust = True
                            continue
                    accepted = False

    def dealer_action(self):
        """
        Automates dealer action. Dealer has different rules than players. Must hit until 17 is achieved.
        Dealer does NOT hit soft 17. Dealer also does not hit if all players bust.
        """
        if all(player.bust for player in self.players if not player.dealer):
            print("All players busted! Dealer stays.")
        else:
            finished = False
            for player in self.players:
                if not player.dealer:
                    continue
                else:
                    print(f"------------------------------------")
                    print(f"{player.name}")
                    print(f"Cards: {player.cards} | Current total: {player.card_total()}")
                    time.sleep(1)
                    while not finished:
                        if any(i == 21 for i in player.card_total()):
                            print("Dealer blackjack!")
                            finished = True
                            player.blackjack = True
                        elif all(i > 21 for i in player.card_total()):
                            print("Dealer busts!")
                            finished = True
                            player.bust = True
                        elif any(i >= 17 and i <= 21 for i in player.card_total()):
                            print("Dealer stays.")
                            finished = True
                        else:
                            player.cards.append(self.deck[0])
                            self.deck.pop(0)
                            print(f"Cards: {player.cards} | Current total: {player.card_total()}")
                        time.sleep(1)

    def current_cards(self):
        """
        Report current cards for each player. However, if player is the dealer, only report second card.
        """
        print(f"------------------------------------")
        for player in self.players:
            if not player.dealer:
                print(f"{player.name}: {player.cards}")
            else:
                print(f"{player.name}: {player.cards[1]}")

    def final_score(self, cards):
        """
        If not busted or blackjack, report the score. Player can have two scores that are valid if they have
        an Ace (for example, A & 9 would be a score of either 20 or 10). If two scores valid, take the highest.
        """
        if max(cards) > 21:
            score = min(cards)
        else:
            score = max(cards)
        return score

    def calc_credits(self):
        """
        Takes dealer final score and compares each players score to it. If dealer has busted,
        dealer score is 0 and anyone who has not busted receives their payout. If a player
        receives blackjack on first two cards, payout is 2x. If dealer and player tie, then
        push is achieved and player receives bet back with no payout. If player's score is
        greater than dealers score, player receives payout equal to bet. If player busts or
        dealer score is higher, player loses bet.

        """
        for player in self.players:
            if player.dealer:
                if player.bust:
                    dealer_score = 0
                else:
                    dealer_score = self.final_score(player.card_total())
        for player in self.players:
            if not player.dealer:
                player_score = self.final_score(player.card_total())
                if len(player.cards) == 2 and player.blackjack:
                    player.payout = player.bet * 2
                    player.credits += player.payout
                elif player.bust or player_score < dealer_score:
                    player.credits -= player.bet
                elif player_score > dealer_score:
                    player.payout = player.bet
                    player.credits += player.bet
                    player.winner = True
                else:
                    player.push = True
                    player.credits = player.credits

    def report_player_scores(self):
        """
        Report the player scores and whether they busted, had blackjack, or pushed.
        """
        print(" ")
        print("########## Hand Scores ##########")
        for player in self.players:
            if not player.dealer:
                if player.bust:
                    print(f"{player.name}: Busted! Loss: {player.bet} | Total credits: {player.credits}")
                elif player.blackjack:
                    print(f"{player.name}: Blackjack! Payout: {player.payout} | Total credits: {player.credits}")
                elif player.push:
                    print(f"{player.name}: Push! | Total credits: {player.credits}")
                elif player.winner:
                    print(
                        f"{player.name}: {self.final_score(player.card_total())} - Winner! Payout: {player.payout} | Total credits: {player.credits}"
                    )
                elif player.bet == 0:
                    print(f"{player.name}: -- | Total credits: {player.credits}")
                else:
                    print(
                        f"{player.name}: {self.final_score(player.card_total())} - Sorry! Loss: {player.bet} | Total credits: {player.credits}"
                    )

    def report_dealer_score(self):
        """
        Report the dealer score and whether they busted or had blackjack.
        """
        for player in self.players:
            if player.dealer:
                if player.bust:
                    print(f"{player.name}: Busted!")
                elif player.blackjack:
                    print(f"{player.name}: Blackjack!")
                else:
                    print(f"{player.name}: {self.final_score(player.card_total())}")
        print("#################################")
        print(" ")

    def bets(self):
        """
        Before each round starts, take the best from each of the players. To be eligible
        to be dealt cards, a player must bet. If player bets 0, they are dealt no cards
        and move to the next round. Player can only bet a maximum of their total credits.
        """
        for player in self.players:
            player.reset()
            if not player.dealer and player.credits > 0:
                bet_accepted = False
                print(f"{player.name}: place your bet! Available credits: {player.credits}")
                while bet_accepted == False:
                    try:
                        bet = int(input())
                        if bet <= player.credits and bet > 0:
                            player.bet = bet
                            player.bet_flag = True
                            bet_accepted = True
                        elif bet == 0:
                            player.bet_flag = False
                            bet_accepted = True
                        else:
                            raise ValueError
                    except ValueError:
                        print("Please enter a number less than or equal to your available credits!")

    def play(self):
        """Run the game!"""
        self.bets()
        self.deal()
        time.sleep(1)
        self.current_cards()
        time.sleep(1)
        self.hit_or_stay()
        time.sleep(1)
        self.dealer_action()
        time.sleep(1)
        self.calc_credits()
        self.report_player_scores()
        self.report_dealer_score()
        time.sleep(1)