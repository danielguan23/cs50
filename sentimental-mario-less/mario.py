

def main():
    # ask for block size
    while True:
        try:
            height = int(input("Height: "))
            if (height >= 1) and (height <= 8):
                break
        except:
            print("", end="")

    for i in range(height):
        space(height - i - 1)
        block(i + 1)
        print("")


def space(int):
    for i in range(int):
        print(" ", end="")


def block(int):
    for i in range(int):
        print("#", end="")


main()