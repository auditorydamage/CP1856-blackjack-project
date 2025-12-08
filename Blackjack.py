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
    # Ace score options are stored in a mini-list
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


def makeBet():
    # Get a bet from the player, make sure it's a valid amount
    # If available money is less than the minimum bet of $5, ask the user to buy in
    # for another $100 of chips; if they refuse for some reason, exit
    money = db.getMoney()
    print(f"Money: ${money:.2f}")
    if money < 5:
        if input(f"You only have ${money:.2f}! Would you like to buy in for $100? (y/n): ") == 'y':
            money += 100
            print(f"Money: ${money:.2f}")
        else:
            print("Alright - come back when you're ready to buy in!")
            print("Bye!")
            exit()
    try:
        while (bet := round(float(input("Bet amount: ")), 2)) > money \
          or bet < 5 or bet > 1000:
                if bet < 5 or bet > 1000:
                    print(f"Not a valid bet amount. Please enter an amount between $5 and $1000.")
                else:
                    print(f"You don't have enough money to make that bet.\n"
                          f"Enter a bet up to ${money:.2f}.")
    except ValueError:
        print(f"Not a valid bet entry. Please enter a numeric value up to ${money:.2f}")
        while (bet := float(input("Bet amount: "))) > money \
          or bet < 5 or bet > 1000:
                if bet < 5 or bet > 1000:
                    print(f"Not a valid bet amount. Please enter an amount between $5 and $1000.")
                else:
                    print(f"You don't have enough money to make that bet.\n"
                          f"Enter a bet up to ${money:.2f}.")
    # once a valid bet has been made, deduct the bet from the total money pool
    money -= bet
    print()
    return bet, money


def handDisplay(cards, hands, player):
    if player == 0:
        print("DEALER'S CARDS:")
    else:
        print("YOUR CARDS:")
    for card in hands[player]:
        print(f"{cards[card][1]} of {cards[card][0]}")
    print()


def scoreCheck(cards, hands, player, aceCheck=False):
    # The logic is a bit tricky here, since the player may want
    # to take 11 points for their first Ace, but the final total may 
    # go over 21. Therefore, calculate the full score beforehand, 
    # and if that doesn't go over 21 with an 11-point Ace, ask the player
    # for their choice. This should only trigger once or twice per hand, as any
    # subsequent Aces would be counted as one point anyway.
    # The dealer will just treat that first Ace as 11 points until
    # aceElevenScore > 21, so their logic is much simpler.

    # First run-through, to get the total without the extra Ace handling
    aceElevenScore = 0
    for card in hands[player]:
        if cards[card][1] == 'Ace':
            if (aceElevenScore + 11) > 21:
                aceElevenScore += cards[card][2][0]
            else:
                aceElevenScore += cards[card][2][1]
        else:
            aceElevenScore += cards[card][2]
    # Second run-through, the one that matters
    score = 0
    for card in hands[player]:
        if cards[card][1] == 'Ace':
            if (score + 11) > 21:
                score += cards[card][2][0]
            elif (score + 11) <= 21 and aceElevenScore > 21:
                score += cards[card][2][0]
            # Ask the player for their choice here; this is short-circuited by default, and will
            # only be fired if player == 1 and aceCheck=True is passed
            elif player == 1 and aceCheck == True:
                while (choice := input(f"Do you want the {cards[card][1]} of {cards[card][0]} to be worth 1 or 11 points? (1/11): ")) != "1" and \
                 choice != "11":
                    print("Invalid choice - please enter 1 or 11.")
                if choice == "1":
                    score += cards[card][2][0]
                else:
                    score += cards[card][2][1]
            else:
                score += cards[card][2][1]
        else:
            score += cards[card][2]
    return score


def playHand(cards, deck, hands, player):
    # dealer's playing logic; hit until score >= 17
    if player == 0:
        while scoreCheck(cards, hands, player) < 17:
            dealCard(deck, hands, player)
        return scoreCheck(cards, hands, player)
    else:
        # If player was initially dealt an Ace, run scoreCheck to 
        # trigger the Ace handling logic and get the player's points preference
        # before dealing the next card; that way, if the player picks 1
        # and stands with a low value, they're stuck with that score
        score = scoreCheck(cards, hands, player, aceCheck=True)
        while input("Hit or stand? (hit/stand): ") == "hit":
            dealCard(deck, hands, player)
            print()
            handDisplay(cards, hands, player)
            if (score := scoreCheck(cards, hands, player, aceCheck=True)) > 21:
                break
        return score


def handResult(playerScore, dealerScore, bet, money):
    # Show hand results, giveth money or taketh money away
    print(f"YOUR POINTS:     {playerScore}\n"
          f"DEALER'S POINTS: {dealerScore}\n")
    if playerScore > 21:
        print("Bust! You lose.")
        db.putMoney(money)
    elif playerScore > dealerScore:
        print("Congratulations. You win!")
        money += bet * 2
        db.putMoney(money)
    elif playerScore < dealerScore and dealerScore > 21:
        print("Dealer busted. You win!")
        money += bet * 2
        db.putMoney(money)
    elif playerScore < dealerScore:
        print("Sorry. You lose.")
        db.putMoney(money)
    else:
        print("Draw!")
        money += bet
        db.putMoney(money)
    print(f"Money: ${money:.2f}")   


def main():

    cards, deck = initialState()
    gameBanner()
    
    # Beginning of hand loop
    while True:

        # If deck has dropped below 10 cards remaining, reshuffle

        if len(deck) < 10:
            deck = shuffleDeck(cards)

        # Have player make a bet (and buy-in if needed)
        bet, money = makeBet()

        # then deal hands. 0 is dealer, 1 is player
        hands = [ [], [] ]
        while len(hands[0]) < 2:
            for player in range(len(hands)):
                dealCard(deck, hands, player) 
        
        # if player has blackjack, don't even bother with the rest
        # of the hand; declare blackjack, pay out
        # 3:2, go directly to ask player whether to play another hand
        if scoreCheck(cards, hands, 1) == 21 and scoreCheck(cards, hands, 0) < 21:
            handDisplay(cards, hands, 1)
            print("Blackjack! You win!")
            money += bet * 2.5
            print(f"Money: ${money:.2f}")
            db.putMoney(money)        
        # Catch the rare case of double blackjacks (I actually got this in testing!)
        elif scoreCheck(cards, hands, 1) == 21 and scoreCheck(cards, hands, 0) == 21:
            handDisplay(cards, hands, 1)
            handDisplay(cards, hands, 0)
            print("Push! Double blackjacks!")
            money += bet
            print(f"Money: ${money:.2f}")
            db.putMoney(money)
        # No blackjack? Play on.
        else:
            # The only time cards are displayed without calling handDisplay()
            print(f"DEALER'S SHOW CARD:")
            print(f"{cards[hands[0][0]][1]} of {cards[hands[0][0]][0]}")
            print()

            handDisplay(cards, hands, 1)
            
            # Player's turn
            playerScore = playHand(cards, deck, hands, 1)
            
            # Dealer's turn; only play if the player doesn't bust, 
            # otherwise just get the dealer's points
            if playerScore <= 21:
                dealerScore = playHand(cards, deck, hands, 0)
            else:
                dealerScore = scoreCheck(cards, hands, 0)
            
            # Once dealer's turn is done, show dealer's hand
            print()
            handDisplay(cards, hands, 0)

            # Display result, pay out money
            handResult(playerScore, dealerScore, bet, money)
            
        print()

        if input("Play again? (y/n): ") != 'y':
            print()
            print("Come back soon!")
            print("Bye!")
            break
        print()


if __name__ == '__main__':
    main()