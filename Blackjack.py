#!/usr/bin/env python3

import random as r
import db


def gameBanner():
    print(f"BLACKJACK!\n"
          f"Blackjack payout is 3:2\n")
    

def initialState():
    # Builds the card deck, does the initial deck shuffle
    cards = []
    suits = ["Hearts", "Diamonds", "Spades", "Clubs"]
    ranks = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", \
             "Queen", "King"]
    points = [[1, 11], 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
    for suit in suits:
        pointCounter = 0
        for rank in ranks:
            cards.append([suit, rank, points[pointCounter]])
            pointCounter += 1
    deck = shuffleDeck(cards)
    return cards, deck


def shuffleDeck(cards):
    # Builds a shuffled deck from the cards list, returns it
    # The actual "deck" built here is a list of integers, 0 through 51, 
    # which act as references to entries in the master cards list. These values
    # are randomly popped into deck from an ordered list, deck_prep
    deck = []
    deck_prep = [x for x in range(len(cards))]
    for x in range(len(cards)):
        deck.append(deck_prep.pop(r.randint(0, len(deck_prep) - 1)))
    return deck


def dealCard(deck, hands, player):
    # Grabs the topmost card from the deck and deals it
    hands[player].append(deck.pop(0))


def makeBet():
    # Get a bet from the player, make sure it's a valid amount
    return


def playerDisplay(cards, hands, player):
    print(f"YOUR CARDS:")
    for card in hands[player]:
        print(f"{cards[card][1]} of {cards[card][0]}")


def scoreCheck(cards, hands, player):
    score = 0
    for card in hands[player]:
        score += cards[card][2]
    print(score)


def main():

    cards, deck = initialState()
    hands = [ [], [] ] # 0 is dealer, 1 is player

    gameBanner()
    
    # Beginning of hand - initial deal
    # overall game loop will start here

    # Make initial bet
    # makeBet()

    # then deal hands
    while len(hands[0]) < 2:
        for player in range(len(hands)):
            dealCard(deck, hands, player)

    print(f"DEALER'S SHOW CARD:")
    print(f"{cards[hands[0][0]][1]} of {cards[hands[0][0]][0]}")
    print()

    # DEBUG: making sure the cards are being properly referenced
    print("DEBUG:")
    print("Dealer cards:")
    print("-contents of hands[0]-")
    print(hands[0])
    print("-referenced entries in cards-")
    print(cards[hands[0][0]], cards[hands[0][1]])
    print()
    print("Player cards:")
    print("-contents of hands[1]-")
    print(hands[1])
    print("-referenced entries in cards-")
    print(cards[hands[1][0]], cards[hands[1][1]])
    
    # player loop will start here

    playerDisplay(cards, hands, 1)

    while input("Hit or stand? (hit/stand): ") == "hit":
           dealCard(deck, hands, 1)
           scoreCheck(cards, hands, 1)
           playerDisplay(cards, hands, 1)
           
    
    # while True:
    #     # main game loop
    #     # make bet
    #     # deal cards to start hand
    #.    # display dealer's show card
    #     while True:
    #         # player's loop
    #         # display player's cards
    #         # hit or stand?
    #         # hit: deal another card, check score for bust
    #         # stand: end player's loop
    #     # show dealer's cards
    #.    # tally and show points
    #.    # win/loss?
    #.    # show money won/lost, record to disk
    #.    # play another hand?

    # temporary game end
    print("Game over man, game over!")


if __name__ == '__main__':
    main()