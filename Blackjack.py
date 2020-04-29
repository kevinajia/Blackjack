#  File: Blackjack.py

#  Description: Simulate a Blackjack game using classes and object-oriented programming

#  Student Name: Kevin Jia

#  Date Created: 2/25/2018

#  Date Last Modified: 2/25/2018

import random


class Card(object):
    RANKS = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13)

    SUITS = ('C', 'D', 'H', 'S')

    # constructor
    def __init__(self, rank=12, suit='S'):
        if (rank in Card.RANKS):
            self.rank = rank
        else:
            self.rank = 12

        if (suit in Card.SUITS):
            self.suit = suit
        else:
            self.suit = 'S'

    # string representation of a Card object
    def __str__(self):
        if self.rank == 1:
            rank = 'A'
        elif self.rank == 13:
            rank = 'K'
        elif self.rank == 12:
            rank = 'Q'
        elif self.rank == 11:
            rank = 'J'
        else:
            rank = self.rank
        return str(rank) + self.suit

    def __eq__(self, other):
        return (self.rank == other.rank)

    def __ne__(self, other):
        return (self.rank != other.rank)

    def __lt__(self, other):
        return (self.rank < other.rank)

    def __le__(self, other):
        return (self.rank <= other.rank)

    def __gt__(self, other):
        return (self.rank > other.rank)

    def __ge__(self, other):
        return (self.rank >= other.rank)


class Deck(object):
    # constructor
    def __init__(self):
        self.deck = []
        for suit in Card.SUITS:
            for rank in Card.RANKS:
                card = Card(rank, suit)
                self.deck.append(card)

    # shuffle the deck
    def shuffle(self):
        random.shuffle(self.deck)

    # deal a card
    def deal(self):
        if len(self.deck) == 0:
            return None
        else:
            return self.deck.pop(0)


class Player(object):
    # cards is a list of card objects
    def __init__(self, cards):
        self.cards = cards

    # when a player hits append a card
    def hit(self, card):
        self.cards.append(card)

    # count the points in the Player's hand
    def getPoints(self):
        count = 0
        for card in self.cards:
            if card.rank > 9:
                count += 10
            elif card.rank == 1:
                count += 11
            else:
                count += card.rank

        # deduct 10 if Ace is there and needed as 1
        for card in self.cards:
            if count <= 21:
                break
            elif card.rank == 1:
                count = count - 10

        return count

    # does the player have blackjack
    def has_blackjack(self):
        return len(self.cards) == 2 and self.getPoints() == 21

    # complete the code that returns the string representation of
    # the cards and points in the hand
    def __str__(self):
        cards = ""
        for card in self.cards:
            cards = cards + " " + str(card)
        cards = cards + " - " + str(self.getPoints()) + " points"
        return cards


# Dealer class inherits from the Player class
class Dealer(Player):
    def __init__(self, cards):
        Player.__init__(self, cards)
        self.show_one_card = True

    # over-ride the hit() function in the parent class
    def hit(self, deck):
        self.show_one_card = False
        while self.getPoints() < 17:
            self.cards.append(deck.deal())

    # return a string showing just one card if not hit yet
    def __str__(self):
        if self.show_one_card:
            return str(self.cards[0])
        else:
            return Player.__str__(self)


class Blackjack(object):
    def __init__(self, numPlayers=1):
        self.deck = Deck()
        self.deck.shuffle()

        # create the number of Player objects
        self.numPlayers = numPlayers
        self.Players = []

        for i in range(self.numPlayers):
            self.Players.append(Player([self.deck.deal(), self.deck.deal()]))

        # create the dealer
        # dealer also gets two cards
        self.dealer = Dealer([self.deck.deal(), self.deck.deal()])

    def play(self):
        # Print the cards that each player has
        for i in range(self.numPlayers):
            print('Player ' + str(i + 1) + ': ' + str(self.Players[i]))

        # Print the cards that the dealer has
        print('Dealer: ' + str(self.dealer))

        # Each player hits until he says no
        playerPoints = []
        for i in range(self.numPlayers):
            while True:
                choice = input("Player " + str(i + 1) + " " + 'do you want to hit? [y / n]: ')
                if choice in ('y', 'Y'):
                    (self.Players[i]).hit(self.deck.deal())
                    points = (self.Players[i]).getPoints()
                    print('Player ' + str(i + 1) + ': ' + str(self.Players[i]))
                    if points >= 21:
                        break
                else:
                    break
            playerPoints.append((self.Players[i]).getPoints())

        # Dealer's turn now
        self.dealer.hit(self.deck)
        dealerPoints = self.dealer.getPoints()
        print('Dealer: ' + str(self.dealer))

        # determine the outcome; this code is written for one player
        # extend it for all players
        for i in range(len(playerPoints)):
            if dealerPoints > 21:
                print('Dealer loses')
                print('All Players Win!')
                break
            if dealerPoints > playerPoints[i]:
                print('Dealer wins')
                break
            elif dealerPoints < playerPoints[i] and playerPoints[i] <= 21:
                print('Player ' + str(i + 1) + ' wins')
                break
            elif dealerPoints == playerPoints:
                if self.Players[i].has_blackjack() and not self.dealer.has_blackjack():
                    print('Player ' + str(i + 1) + ' wins')
                    break
                elif not self.Players[i].has_blackjack() and self.dealer.has_blackjack():
                    print('Dealer wins')
                    break
                else:
                    print('There is a tie')


def main():
    # prompt the user to enter the number of players
    num_players = eval(input('Enter number of players: '))
    while (num_players < 1 or num_players > 6):
        num_players = eval(input('Enter number of players: '))

    # create the Blackjack object
    game = Blackjack(num_players)

    # play the game
    game.play()


main()
