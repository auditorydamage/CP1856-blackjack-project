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
    points = [[1, 11], 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
    for suit in suits:
        pointCounter = 0
        for rank in ranks:
            cards.append([suit, rank, points[pointCounter]])
            pointCounter += 1
    deck = shuffleDeck(cards)
    money = db.getMoney()
    return cards, deck, money


def shuffleDeck(cards):
    # Builds a shuffled deck from the cards list, returns it
    # The actual "deck" built here is a list of integers, 0 through 51, 
    # which act as references to entries in the master cards list. These values
    # are randomly popped into deck from an ordered list, deck_prep, which
    # is just a series of integers the same length as the list of cards
    deck = []
    deck_prep = [x for x in range(len(cards))]
    for x in range(len(cards)):
        deck.append(deck_prep.pop(r.randint(0, len(deck_prep) - 1)))
    return deck


def dealCard(deck, hands, player):
    # Grabs the topmost card from the deck and deals it
    hands[player].append(deck.pop(0))


def makeBet(money):
    # Get a bet from the player, make sure it's a valid amount
    print(f"Money: {money}")
    while (bet := int(input("Bet amount: "))) > money:
        print(f"You don't have enough money to make that bet.\n"
              f"Enter a bet up to ${money}.")
    return bet


def handDisplay(cards, hands, player):
    if player == 0:
        print("DEALER'S CARDS:")
    else:
        print("YOUR CARDS:")
    for card in hands[player]:
        print(f"{cards[card][1]} of {cards[card][0]}")
    print()


def scoreCheck(cards, hands, player):
    # First loop gets the total score with Ace = 11 points
    fullAceScore = 0
    for card in hands[player]:
        if cards[card][1] == 'Ace':
            fullAceScore += cards[card][2][1]
        else:
            fullAceScore += cards[card][2]
    # Second loop checks against fullAceScore; if > 21, Ace = 1 point
    score = 0
    for card in hands[player]:
        if cards[card][1] == 'Ace':
            if fullAceScore > 21:
                score += cards[card][2][0]
            else:
                score += cards[card][2][1]
        else:
            score += cards[card][2]
    return score


def playHand(cards, deck, hands, player):
    # the hand playing logic; if dealer, hit until score >= 17
    if player == 0:
        while scoreCheck(cards, hands, player) < 17:
            dealCard(deck, hands, player)
    else:
        while input("Hit or stand? (hit/stand): ") == "hit":
            dealCard(deck, hands, player)
            handDisplay(cards, hands, player)
            if scoreCheck(cards, hands, player) > 21:
                break
            print()

# def handResult(playerScore, dealerScore, bet):
    # show results, pay out winnings, update wallet
#    return


def main():

    cards, deck, money = initialState()
    gameBanner()
    
    # Beginning of hand - initial deal
    
    while True:

        # Track number of hands dealt; if hands reaches 15, or the deck
        # drops below 10 cards remaining, reshuffle
        # Make initial bet
        bet = makeBet(money)

        # then deal hands. 0 is dealer, 1 is player
        hands = [ [], [] ]
        while len(hands[0]) < 2:
            for player in range(len(hands)):
                dealCard(deck, hands, player) 
        
        # if player has blackjack, don't even bother with the rest
        # of the player loop and aftermath; declare blackjack, pay out
        # 3:2, go directly to ask player whether to play another hand
        if scoreCheck(cards, hands, 1) == 21 and scoreCheck(cards, hands, 0) < 21:
            handDisplay(cards, hands, 1)
            print("Blackjack! You win!")
        # Catch the rare case of double blackjacks (I actually got this in testing!)
        elif scoreCheck(cards, hands, 1) == 21 and scoreCheck(cards, hands, 0) == 21:
            handDisplay(cards, hands, 1)
            handDisplay(cards, hands, 0)
            print("Draw! Double blackjacks!")
        # No blackjack? Play on.
        else:
            # The only time cards are displayed without calling handDisplay()
            print(f"DEALER'S SHOW CARD:")
            print(f"{cards[hands[0][0]][1]} of {cards[hands[0][0]][0]}")
            print()
            handDisplay(cards, hands, 1)
            # Player's hand
            playHand(cards, deck, hands, 1)
            # Dealer's hand; only play if the player doesn't bust
            if scoreCheck(cards, hands, 1) <= 21:
                playHand(cards, deck, hands, 0)
            
            handDisplay(cards, hands, 0)

            playerScore = scoreCheck(cards, hands, 1)
            dealerScore = scoreCheck(cards, hands, 0)
            print(f"YOUR POINTS:     {playerScore}\n"
                  f"DEALER'S POINTS: {dealerScore}\n")

            # Add money handling, maybe move this into its own function
            # handResult(playerScore, dealerScore, bet)
            if playerScore > 21:
                print("Bust! You lose.") 
            elif playerScore > dealerScore:
                print("Congratulations. You win!")
            elif playerScore < dealerScore and dealerScore > 21:
                print("Dealer busted. You win!")
            elif playerScore < dealerScore:
                print("Sorry. You lose.")
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