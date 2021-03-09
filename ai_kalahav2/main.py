# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from random import randrange


def print_board(show_players):
    print("\t", end="")
    print("[", end="")
    for item in range(1, 6):
        print("%2d, " % myBoard[item], end="")
    print("%2d]" % myBoard[6], end="")
    if show_players:
        print(" <- Player 1")
    else:
        print("")

    print("\t[%2d]\t\t\t\t[%2d]" % (myBoard[0], myBoard[7]))

    print("\t[", end="")
    for item in range(8, 13):
        print("%2d, " % myBoard[item], end="")
    print("%2d]" % myBoard[13], end="")

    if show_players:
        print(" <- Player 2")
    else:
        print("")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    myBoard = [0]

    # Make 14 fields, 0 and 7 will be player pots, we add 6 to all holes
    for i in range(0, 13):
        myBoard.append(6)

    # And change the pots to 0
    myBoard[0] = 0
    myBoard[7] = 0

    # Here we initialize some of the variables needed to keep track of the game
    in_hand = 0
    run = True
    playerNum = 1
    playerIn = 0
    # used for checking who wins
    pl1sum = 0
    pl2sum = 0
    while run:

        print_board(True)
        valid_move = False
        while not valid_move:
            if playerNum == 2:
                playerIn = randrange(6)
            else:
                playerIn = int(input("Player %i make a move: " % playerNum))
            if playerNum == 2:
                playerIn += 7
            playerIn = playerIn % 14
            if myBoard[playerIn] == 0:
                print("Invalid move, piece is empty")
            elif playerIn == 0 or playerIn == 7:
                print("Invalid move, this is a player pot, cant start from here!")
            else:
                valid_move = True

        in_hand = myBoard[playerIn]
        myBoard[playerIn] = 0

        currentPos = playerIn

        while in_hand != 0:
            if currentPos < 8:
                currentPos -= 1
            else:
                currentPos += 1

            if currentPos == -1:
                currentPos = 8

            if currentPos == 14:
                currentPos = 7

            if playerNum == 1 and currentPos == 7:
                currentPos -= 1

            if playerNum == 2 and currentPos == 0:
                currentPos = 8

            myBoard[currentPos] += 1
            in_hand -= 1

            if in_hand == 0 and myBoard[currentPos] > 1 and currentPos != 0 and currentPos != 7:
                in_hand = myBoard[currentPos]
                myBoard[currentPos] = 0

            print_board(False)
            print("Left in hand: %d" % in_hand)

        print("Ended at position %d!" % currentPos)

        # Check player 1's side, if it's empty we call game over
        pl1sum = 0
        pl2sum = 0
        for i in range(1, 7):
            pl1sum += myBoard[i]
        for i in range(8, 14):
            pl2sum += myBoard[i]
        if pl1sum == 0:
            print("Game over!")
            run = False
            myBoard[0] += pl2sum
        if pl2sum == 0:
            print("Game over!")
            run = False
            myBoard[7] += pl1sum

        print("Balls at pl1: %d and pl2: %d" % (pl1sum, pl2sum))

        # if we end at a player pit it means the same player can go again so we don't change the playerNum
        if currentPos != 0 and currentPos != 7:
            if playerNum == 1:
                playerNum = 2
            else:
                playerNum = 1

    print_board(True)

    if myBoard[0] > myBoard[7]:
        print("Player 1 wins with %d balls!\nPlayer 2 had %d balls!" % (myBoard[0], myBoard[7]))
        print("%d balls was stolen from the other player!" % pl2sum)
    else:
        print("Player 2 wins with %d balls!\nPlayer 1 had %d balls!" % (myBoard[7], myBoard[0]))
        print("%d balls was stolen from the other player!" % pl1sum)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
