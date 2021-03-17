# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from random import randrange
import copy


class Board:

    def __init__(self, board_state, player_turn_in, parent_in):
        self.myBoard = board_state
        self.currPos = 0
        self.done = False
        self.player_turn = player_turn_in
        self.parent = parent_in
        self.children = []
        self.state_copy = None
        self.util = 0
        # Make 14 fields, 0 and 7 will be player pots, we add 6 to all holes
        if len(board_state) == 0:
            for ii in range(0, 14):
                self.myBoard.append(4)
            # And change the pots to 0
            self.myBoard[0] = 0
            self.myBoard[7] = 0

    def move_pot(self, pot):
        if pot < 1 or pot > 14 or pot == 7:
            print("Error! Illegal move")
            return
        if self.player_turn == 1 and pot > 8:
            print("Illegal move, potnum choose from your side pls")
            return
        if self.player_turn == 2 and pot < 8:
            print("Illegal move, potnum choose from your side pls")
            return

        hand = self.myBoard[pot]
        if hand == 0:
            print("Empty pot, try again")
            return
        self.myBoard[pot] = 0

        self.currPos = pot

        while hand != 0:
            if self.currPos < 8:
                self.currPos -= 1
            else:
                self.currPos += 1

            if self.currPos == -1:
                self.currPos = 8

            if self.currPos == 14:
                self.currPos = 7

            if self.player_turn == 1 and self.currPos == 7:
                self.currPos -= 1

            if self.player_turn == 2 and self.currPos == 0:
                self.currPos = 8

            self.myBoard[self.currPos] += 1
            hand -= 1

            if hand == 0 and self.myBoard[self.currPos] > 1 and self.currPos != 0 and self.currPos != 7:
                hand = self.myBoard[self.currPos]
                self.myBoard[self.currPos] = 0

        if self.currPos != 0 and self.currPos != 7:
            if self.player_turn == 1:
                self.player_turn = 2
            else:
                self.player_turn = 1

        pl1sum = 0
        pl2sum = 0
        for i in range(1, 7):
            pl1sum += self.myBoard[i]
            pl2sum += self.myBoard[i+7]

        if pl1sum == 0:
            print("Game over!")
            self.done = True
            self.myBoard[0] += pl2sum
        if pl2sum == 0:
            print("Game over!")
            self.done = True
            self.myBoard[7] += pl1sum
        if self.done:
            for i in range(1, 7):
                self.myBoard[i] = 0
                self.myBoard[i+7] = 0

        return self

    def print_the_board(self, show_player_sides, show_turn, show_help, show_util_val):
        if show_help:
            print("\t ", end="")
            for x in range(1, 7):
                print("%2d  " % x, end="")
            print("")
        print("\t[", end="")
        for item in range(1, 6):
            print("%2d, " % self.myBoard[item], end="")
        print("%2d]" % self.myBoard[6], end="")

        if show_player_sides:
            print(" <- Player 1")
        else:
            print("")

        print("\t[%2d]                [%2d]\n\t[" % (self.myBoard[0], self.myBoard[7]), end="")

        for item in range(8, 13):
            print("%2d, " % self.myBoard[item], end="")
        print("%2d]" % self.myBoard[13], end="")

        if show_player_sides:
            print(" <- Player 2")
        else:
            print("")
        if show_help:
            print("\t ", end="")
            for x in range(8, 14):
                print("%2d  " % x, end="")
            print("")
        if show_turn:
            print("\tPlayer turn: %d" % self.player_turn)
        if show_util_val:
            print("\tUtil value: %f" % self.util)

    def print_children(self):
        print("Printing children:")
        for x in self.children:
            if x is not None:
                x.print_the_board(False, True, False, True)
                print("")
            else:
                print("empty child, you failed somewhere")


    def find_util(self):
        # Used to find the amount of balls on either side
        my_side = 0
        other_side = 0

        # Count the balls
        for ii in range(1, 7):
            other_side += self.myBoard[ii]
        for ii in range(8, 14):
            my_side += self.myBoard[ii]

        # Find the util/heuristric value
        self.util = (self.myBoard[7]-self.myBoard[0]) + (self.player_turn-1) * 10 + (my_side-other_side)

    # Add possible children, we have 6 possible moves per side so depending on the turn
    def generate_children(self, depth, start_depth, print_info):
        if print_info:
            print("Depth: %d" % depth)

        # If we are at the end we return
        if depth == 0:
            return self

        # Make sure we only check valid moves for each player
        for ii in range(1, 7):
            ii_copy = ii
            if self.player_turn == 2:
                ii_copy += 7

            if self.myBoard[ii_copy] != 0:
                # Create a new "node"/"board"
                new_node = Board(copy.deepcopy(self.myBoard), self.player_turn, self)
                if print_info:
                    print("Based on: %d\nNew_node: \t%s\nSelf: \t\t%s\nParent: \t%s" % (ii_copy, str(new_node), str(self), str(self.parent)))
                    new_node.print_the_board(False, True, False, False)

                # Move pieces in the new node based on ii
                new_node.move_pot(ii_copy)

                # Assign a inf number based on the player turn
                if new_node.player_turn == 2:
                    new_node.util = float("inf")
                else:
                    new_node.util = float("-inf")
                if print_info:
                    new_node.print_the_board(False, True, False, False)


                # Generate children for the new node if it's not a "goal state"
                if not new_node.done:
                    new_node.find_util()
                    new_node.generate_children(depth - 1, start_depth + 1, print_info)
                elif depth - 1 == 0:
                    # If it's the last node we generate a util value
                    new_node.find_util()
                # After children are done we add the new_node to children list of it's parent
                self.children.append(new_node)


class AI:

    def __init__(self, depth_in):
        self.depth = depth_in
        self.state = Board([], 1, None)
        self.head = None

    def find_children(self, print_children, depth_in, board_in):
        self.state = copy.deepcopy(board_in)
        if depth_in <= 0:
            return self.state.generate_children(self.depth, 0, print_children)
        else:
            return self.state.generate_children(depth_in, 0, print_children)

    def print_head(self):
        self.state.print_children()
        print("Second child's children:")
        self.state.children[2].print_children()
        print("Third child's children:")
        self.state.children[2].children[0].print_children()

    def best_move(self):
        print("Returning bullshit value!")
        if self.state.player_turn == 2:
            return randrange(8, 14)
        else:
            return randrange(1, 7)

    def minimax(self, state_in, max_depth, is_max):
        # 1: find children, then find children from that layer and so on.. until we reach a certain depth
        # 2: when at depth stop and return the util value.
        # 3: ripple this value up
        # self.find_children()

        # If at the buttom/max depth return the util value
        if max_depth == 0:
            return self.util(state_in)

        # Generate children fo this state
        self.find_children(state_in)
        # if we look for max return the best move
        if is_max:
            max_val = float('-inf')
            best_state = None
            for child in state_in.children:
                self.minimax(child)
                if max_val < child.util:
                    max_val = child.util
                    best_state = child
            return self.minimax(child, max_depth-1, True)
        else:
            min_val = float('inf')
            best_state = None
            for child in state_in.children:
                if min_val > child.util:
                    min_val = child.util
                    best_state = child
            return self.minimax(child, max_depth-1, False)


if __name__ == '__main__':
    the_board = Board([], 1, None)
    the_AI = None
    against_ai = False
    user_in = int(input("Game_mode:\n1. 1-Player vs. AI\n2. 2-Player\nChoose: "))
    if user_in == 1:
        the_AI = AI(5)
        against_ai = True

    what_to_move = 0
    while not the_board.done:
        the_board.print_the_board(True, False, True, False)
        what_to_move = 0
        print("Player %d make a move!" % the_board.player_turn)
        if against_ai and the_board.player_turn == 2:
            print("AI doing things:")

            last_node = the_AI.find_children(False, 3, the_board)
            print("last_node: %s" % str(last_node))
            # last_node.print_first_child()
            what_to_move = the_AI.best_move()
        else:
            what_to_move = int(input("What pot do you want to move from? : "))
        print("Moving from pot: %d!" % what_to_move)
        the_board.move_pot(what_to_move)
    the_board.print_the_board(True, False, False, False)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
