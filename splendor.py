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
    return line[:-1]

class Player:
    def __init__(self, name=None, ai=True):
        self.ai = ai
        self.name = name if name is not None else random_line(open("names.txt"))
        self.blue = 0
        self.green = 0
        self.red = 0
        self.white = 0
        self.black = 0
        self.gold = 0
        self.cards = []
        self.reserve = []

    def give_token(self, color, n):
        i = getattr(self, color)
        setattr(self, color, i+n)
        return getattr(self, color)

    def card_list(self):
        return " ".join([card.gem for card in self.cards])

    def __str__(self):
        u = "" if self.blue == 0 else f"{self.blue}u "
        g = "" if self.green == 0 else f"{self.green}g "
        r = "" if self.red == 0 else f"{self.red}r "
        k = "" if self.black == 0 else f"{self.black}k "
        w = "" if self.white == 0 else f"{self.white}w "
        o = "" if self.gold == 0 else f"{self.gold}o "
        s = f"(gem stash: {u}{g}{r}{k}{w}{o})\n cards: {self.card_list()}\n reserve: {self.reserve}"
        return s

    @property
    def pts(self):
        return sum(card.pts for card in self.cards)

    def make_choice(self):
        if self.ai:
            options = [
                ("three gems", random.choices(TOKENS, k=3)),
                ("two gems", random.choice(TOKENS)),
                ("purchase", random.randint(1,3), random.randint(1,4)),
                ("reserve", random.randint(1,4))
            ]
            return random.choice(options)
        # player input
        decision = input("What do you want to do? ")
        decision = decision.split(" ")
        if decision[0] in ("purchase", "reserve"):
            return (decision[0], int(decision[1]), int(decision[2]))
        if len(decision) == 3:
            return ("three gems", *decision)
        if len(decision) == 1:
            return ("two gems", *decision)
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

    def __str__(self):
        u = "" if self.blue == 0 else f"{self.blue}u "
        g = "" if self.green == 0 else f"{self.green}g "
        r = "" if self.red == 0 else f"{self.red}r "
        k = "" if self.black == 0 else f"{self.black}k "
        w = "" if self.white == 0 else f"{self.white}w "
        s = f"({self.gem} {self.pts}pts {u}{g}{r}{k}{w})"
        return s
    def __repr__(self):
        return str(self)

class Noble:
    def __init__(self, blue, green, red, white, black, pts=3):
        self.pts = pts
        self.blue = blue
        self.green = green
        self.red = red
        self.white = white
        self.black = black

    def __str__(self):
        u = "" if self.blue == 0 else f"{self.blue}u "
        g = "" if self.green == 0 else f"{self.green}g "
        r = "" if self.red == 0 else f"{self.red}r "
        k = "" if self.black == 0 else f"{self.black}k "
        w = "" if self.white == 0 else f"{self.white}w "
        s = f"({self.pts}pts {u}{g}{r}{k}{w})"
        return s

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
    random.shuffle(data["level_one"])
    random.shuffle(data["level_two"])
    random.shuffle(data["level_three"])
    level_one_deck = [DevCard(card["gem"], card["points"], card["blue"],
                    card["green"], card["red"], card["white"], card["black"]
                    ) for card in data["level_one"]]
    level_two_deck = [DevCard(card["gem"], card["points"], card["blue"],
                    card["green"], card["red"], card["white"], card["black"]
                    ) for card in data["level_two"]]
    level_three_deck = [DevCard(card["gem"], card["points"], card["blue"],
                    card["green"], card["red"], card["white"], card["black"]
                    ) for card in data["level_three"]]
    nobles = [Noble(n["blue"], n["green"], n["red"], n["white"], n["black"]
                ) for n in random.choices(data["nobles"], k=num_players+1)]
    game_over = False
    players = [Player(ai=False) for i in range(num_players)]
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
            print(f"\n{player.name}'s turn. {player.pts} points")
            print("nobles", *nobles)
            print(*level_three_deck[0:4])
            print(*level_two_deck[0:4])
            print(*level_one_deck[0:4])
            print(player)

            decision = player.make_choice()
            print(decision)

            # update game state
            if decision[0] == "three gems":
                for color in decision[1:]:
                    player.give_token(color, 1)
                    supply[color] -= 1
            elif decision[0] == "two gems":
                color = decision[1]    
                player.give_token(color, 2)
                supply[color] -= 2
            elif decision[0] == "purchase":
                mapping = {0: player.reserve, 1: level_one_deck, 2: level_two_deck, 3:level_three_deck}
                card = mapping[decision[1]].pop(decision[2]-1)
                player.cards.append(card)
                pass
            elif decision[0] == "reserve":
                mapping = {1: level_one_deck, 2: level_two_deck, 3:level_three_deck}
                card = mapping[decision[1]].pop(decision[2]-1)
                player.reserve.append(card)
                player.gold += 1
            else:
                print("ERROR")

            # check game over condition
            check_game_over(players)
    # find out who won and print it

if __name__ == "__main__":
    main()
