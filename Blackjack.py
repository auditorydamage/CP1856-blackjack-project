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
    # re-add a mini-list in [0] for the Ace score options
    points = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
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


def handDisplay(cards, hands, player):
    if player == 0:
        print("DEALER'S CARDS:")
    else:
        print("YOUR CARDS:")
    for card in hands[player]:
        print(f"{cards[card][1]} of {cards[card][0]}")
    print()


def scoreCheck(cards, hands, player):
    score = 0
    for card in hands[player]:
        # add logic here for the Ace point options
        score += cards[card][2]
    return score


def main():

    cards, deck = initialState()
    gameBanner()
    
    # Beginning of hand - initial deal
    
    while True:

        # Track number of hands dealt; if hands reaches 15, or the deck
        # drop below 10 cards remaining, reshuffle
        # Make initial bet
        # makeBet()

        # then deal hands. 0 is dealer, 1 is player
        hands = [ [], [] ]
        while len(hands[0]) < 2:
            for player in range(len(hands)):
                dealCard(deck, hands, player)

        print(f"DEALER'S SHOW CARD:")
        print(f"{cards[hands[0][0]][1]} of {cards[hands[0][0]][0]}")
        print()

        # DEBUG: making sure the cards are being properly referenced
        # print("DEBUG:")
        # print("Dealer cards:")
        # print("-contents of hands[0]-")
        # print(hands[0])
        # print("-referenced entries in cards-")
        # print(cards[hands[0][0]], cards[hands[0][1]])
        # print()
        # print("Player cards:")
        # print("-contents of hands[1]-")
        # print(hands[1])
        # print("-referenced entries in cards-")
        # print(cards[hands[1][0]], cards[hands[1][1]])

        handDisplay(cards, hands, 1)

        while input("Hit or stand? (hit/stand): ") == "hit":
           dealCard(deck, hands, 1)
           handDisplay(cards, hands, 1)
           if scoreCheck(cards, hands, 1) > 21:
               break
           print()

        # Once player's turn is done, run the dealer's play, then show
        # the outcome. TODO: implement dealer's play.
        handDisplay(cards, hands, 0)

        playerScore = scoreCheck(cards, hands, 1)
        dealerScore = scoreCheck(cards, hands, 0)
        print(f"YOUR POINTS:     {playerScore}\n"
              f"DEALER'S POINTS: {dealerScore}\n")

        # Add money handling, move this into its own functilon
        if playerScore > 21:
            print("Bust! You lose.") 
        elif playerScore > dealerScore:
            print("Congratulations. You win!")
        elif playerScore < dealerScore and dealerScore > 21:
            print("Dealer busted. You win!")
        elif playerScore < dealerScore:
            print("Sorry, You lose.")
        else:
            print("Draw!")
        print()

        # DEBUG: show remaining size of deck
        print(f"Deck cards remaining: {len(deck)}")

        if input("Play again? (y/n): ") == 'n':
            print()
            print("Come back soon!")
            print("Bye!")
            break


if __name__ == '__main__':
    main()