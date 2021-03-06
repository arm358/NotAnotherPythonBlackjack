from deck import Deck
from player import Player
from game import Game
import json
import os


def intial_inputs():
    """
    Take player names and number of decks to play with.
    Minimum number of players is 1. Cannot use the name "Dealer"
    Minimum decks to play with is 1 and maximum is 8.

    """
    participants_accepted = False
    decks_accepted = False
    # Take the names of all players. 
    print("Please enter player names separated by a comma.")
    while participants_accepted == False:
        participants = input().replace(" ", "")
        participants = participants.split(",")
        if participants != "" and all(name != "Dealer" for name in participants):
            participants_accepted = True
        else:
            print("Please try again. Enter player names separated by a comma. Cannot use <Dealer> as a name!")
    print("Please enter number of decks. Minimum of 1 deck required, maximum of 8")
    while decks_accepted == False:
        try:
            deck_count = int(input())
            if deck_count >= 1 and deck_count <= 8:
                decks_accepted = True
            else:
                print("Please try again. Enter number of decks. Min = 1 / Max = 8")
        except:
            print("Please try again. Enter number of decks.")

    return participants, deck_count


def set_players(names, scores):
    """
    Instantiate player classes for each player given in the inputs.
    Also instantiate another player class to act as the dealer with no credits.

    """
    players = []
    for player in names:
        if player in scores:
            players.append(Player(player, False, credits=scores[player]+10))
        else:
            players.append(Player(player, credits = 10))
    players.append(Player("Dealer", True, credits=0))
    return players


def game_ends(deck, players, deck_count):
    """
    Check whether we should end the game. Game ends when all players
    are out of credits, or the deck is down to 25% of its original number
    of cards
    """
    if all(player.credits == 0 for player in players) or (len(deck) <= 0.25 * deck_count * 52):
        return True
    else:
        return False


if __name__ == "__main__":

    if os.path.isfile("running_scores.json") and os.stat("running_scores.json").st_size != 0:
          with open("running_scores.json", "r") as file:
            scores = json.load(file)
    else:
        scores = {}
    participants, deck_count = intial_inputs()
    deck = Deck(deck_count).shuffle()
    players = set_players(participants, scores)
    game = Game(players, deck)

    while not game_ends(deck, players, deck_count):
        game.play()
    
    final_scores = {}
    with open("running_scores.json", "w+") as outfile:
        for player in players:
            if not player.dealer: scores[player.name] = player.credits
        json.dump(scores, outfile)

    print("Round over! Thanks for playing.")
