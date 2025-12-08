#!/usr/bin/env python3

def getMoney():
    # Read the player's wallet, or create one if none exists
    # Also catch the case of the wallet file containing a non-numeric
    # value and create a new wallet with $100.
    try:
        with open("wallet", "r") as walletfile:
            money = float(walletfile.read())
    except FileNotFoundError:
        print("Wallet not found - creating new wallet with $100.")
        money = 100.0
        putMoney(money)
    except ValueError:
        print("Invalid value from wallet - starting with $100.00.")
        money = 100.0
        putMoney(money)
    return money


def putMoney(amount):
    # Update the player's wallet
    with open("wallet", "w") as walletfile:
        walletfile.write(str(amount))