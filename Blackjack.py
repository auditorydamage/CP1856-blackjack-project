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


def main():

    cards, deck = initialState()
    hands = [ [], [] ] # 0 is dealer, 1 is player

    gameBanner()
    
    # Beginning of hand - initial deal
    while len(hands[0]) < 2:
        for player in range(len(hands)):
            dealCard(deck, hands, player)

    print(f"DEALER'S SHOW CARD:")
    print(f"{cards[hands[0][1]][1]} of {cards[hands[0][0]][0]}")
    print()
    
    print(f"YOUR CARDS:")
    for card in hands[1]:
        print(f"{cards[card][1]} of {cards[card][0]}")
    
    
    
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


if __name__ == '__main__':
    main()