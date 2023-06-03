from cs50 import get_float
from math import floor


def main():
    while True:
        dollars = get_float("Change owed: ")
        cents = floor(dollars * 100)

        if cents > 0:
            break

    quarters = cents // 25
    remainder = cents - quarters * 25

    dimes = remainder // 10
    remainder = remainder - dimes * 10

    nickels = remainder // 5
    remainder = remainder - nickels * 5

    pennies = remainder
    remainder = remainder - pennies * 1

    print(f"{quarters + dimes + nickels + pennies}")


main()