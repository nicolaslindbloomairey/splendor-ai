""" splendor.py

does the game logic for the game splendor

gameplay

    - each player takes one of 4 possible actions
        - one of each of 3 different colors of gems
        - two of one color
        - reserve a dev card and take gold
        - purchase dev card
"""

import random
import json

TOKENS = ("red", "blue", "green", "white", "black")

def random_line(afile):
    line = next(afile)
    for num, aline in enumerate(afile, 2):
        if random.randrange(num):
            continue
        line = aline
    return line

class Player:
    def __init__(self, name=random_line(open("names.txt")), ai=True):
        self.ai = ai
        self.name = name
        self.blue = 0
        self.green = 0
        self.red = 0
        self.white = 0
        self.black = 0
        self.gold = 0
        self.cards = []
        self.reserve = []

    @property
    def pts(self):
        return sum(card.pts for card in self.cards)

    def make_choice(self):
        if ai:
            options = [
                ("three gems", random.choices(TOKENS, k=3)),
                ("two gems", random.choice(TOKENS)),
                ("purchase", random.randint(1,3), random.randint(1,4)),
                ("reserve", random.randint(1,4))
            ]
            return random.choice(options)
        # player input
        decision = input("What do you want to do?")
        return ("three gems", ["red", "blue", "green"])

class DevCard:
    def __init__(self, gem, pts, blue, green, red, white, black):
        self.gem = gem
        self.pts = pts
        self.blue = blue
        self.green = green
        self.red = red
        self.white = white
        self.black = black

def check_game_over(players):
    game_over = False
    for player in players:
        if player.pts >= 15:
            game_over = True
            return game_over
    return game_over

def main(num_players=2):
    # initialize the game
    with open("cards.json") as f:
        data = json.load(f)
    level_one_deck = data["level_one"]
    level_two_deck = data["level_two"]
    level_three_deck = data["level_three"]
    nobles = random.choices(data["nobles"], k=num_players+1)
    game_over = False
    players = [Player() for i in range(num_players-1)]
    players.append(Player(ai=False))
    supply = {
        "blue": 7,
        "green": 7,
        "red": 7,
        "white": 7,
        "black": 7,
        "gold": 7
    }

    while not game_over:
        for player in players:
            # get player decision
            decision = player.make_choice()

            # update game state
            if decision[0] == "three gems":
                for color in decision[1]:
                    player[color] += 1
                    supply[color] -= 1
            elif decision[0] == "two gems":
                color = decision[1]    
                player[color] += 2
                supply[color] -= 2
            elif decision[0] == "purchase":
            elif decision[0] == "reserve":
                player.gold += 1
            else:
                print("ERROR")

            # check game over condition
            check_game_over()
    # find out who won and print it

if __name__ == "__main__":
    main()
