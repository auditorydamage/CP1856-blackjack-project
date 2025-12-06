#!/usr/bin/env python3

def getMoney():
    # Read the player's available money, or create one if none exists
    try:
        with open("wallet", "r") as walletfile:
            money = int(walletfile.read())
    except FileNotFoundError:
        money = 100
        print("Wallet not found - creating new wallet with $100.")
        with open("wallet", "w") as walletfile:
            walletfile.write(str(money))
    except ValueError:
        print("Invalid value from wallet - starting with $100.00.")
        money = 100
    return money


def putMoney(amount):
    # Update the player's wallet
    with open("wallet", "w") as walletfile:
        walletfile.write(str(amount))
    return