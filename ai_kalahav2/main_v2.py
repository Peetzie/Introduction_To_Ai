# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import copy

class Node:
    total_nodes = 0
    def __init__(self, value_in=0, turn_in = 1):
        self.value = value_in       # value of current node
        self.boardState = []        # board for this node
        self.children = []      # list of children
        self.parent = None
        self.turn = turn_in
        self.last_move = -1
        self.util = -999999
        self.best_node = None
        self.done = False
        Node.total_nodes += 1


class CoolTree:
    def __init__(self):
        self.head = None

    def insert_node(self, value, ball_count):
        new_node = Node(value)
        new_node.parent = self.head
        setup_start_board(new_node.boardState, ball_count)
        if self.head is None:
            self.head = new_node
        else:
            self.head.children.append(new_node)
        return new_node

    def call_child_print(self, depth):
        print("printing children:")
        print_children(self.head, depth)

def print_children(self, depth):
    indent = ""
    for x in range(0, depth):
        # print("- ", end="")
        indent += "----"
    print_state(self, indent, True, True, True)
    if self.children:
        for child in self.children:
            print_children(child, depth+1)

def print_parents(self):
    print("Last move: " + str(self.last_move) + " Self location: " + str(self), end="")
    if self.parent is not None:
        print(" Parent: " + str(self.parent))
        print_parents(self.parent)
    else:
        print("")

def insert_at_node(self, value):
    new_node = Node(value, self.turn)
    new_node.parent = self
    new_node.boardState = self.boardState.copy()
    self.children.append(new_node)
    return new_node

def print_state(self, indent, print_indexes, print_turn = False, print_util = False):
    print(indent,end="")
    if print_indexes:
        print(" ", end="")
        for i in range(12, 6, -1):
            print("%2d " % i, end="")
        print("\n"+indent,end="")
    print("[", end="")
    for i in range(12, 6, -1):
        print("%2d " % self.boardState[i], end="")
    print("]\n" + indent,end="")
    # print("%2d\t\t%2d" % (self[6], self[13]))
    print("[%2d " % (self.boardState[13]), end="")
    print("   "* 4, end="")
    print("%2d ]" % (self.boardState[6]))
    print(indent + "[",end="")
    for i in range(0, 6):
        print("%2d " % self.boardState[i], end="")
    print("]")
    if print_indexes:
        print(indent + " ",end="")
        for i in range(0, 6):
            print("%2d " % i, end="")
        print("")
    print("Last move: %d" % self.last_move, end="")
    if print_turn:
        print(" Turn: %d " % self.turn, end= "")
    if print_util:
        print(" Util: %d" % self.util, end="")
    print("\n")

def setup_start_board(self, ball_count):
    for i in range(0,14):
        self.append(ball_count)
    self[6] = 0
    self[13] = 0

# Calculates a heuristic value based on 2 things; turn and how many balls in the pots
def calc_util(node_in):
    pl1_side = 0
    pl2_side = 0
    for x in range(0, 6):
        pl1_side += node_in.boardState[x]
    for x in range(7, 13):
        pl2_side += node_in.boardState[x]

    return -node_in.boardState[6] + node_in.boardState[13] + (node_in.turn - 1) * 10

# Creates children recursively until depth is met, it will create based on the balls in the different pits
# meaning children will be created if there's balls and not if empty
def create_children(self, depth):
    if depth == 0:
        # If we are at the bottom we can calculate the util value
            # self.util = calc_util(self)
        # However we don't want to this, this is because it takes time and when we scale it bigger this
        # becomes a problem, also we should do it in the minimax algorithm
        return

    # If this node is done, we wont create any children or anything
    if self.done:
        return

    possible_moves = 0
    if self.turn == 1:
        for space in range(0, 6):
            if self.boardState[space] != 0:
                possible_moves += 1
                new_node = insert_at_node(self, self.value+1)
                move_balls(new_node, space)
                create_children(new_node, depth-1)
    else:
        for space in range(7, 13):
            if self.boardState[space] != 0:
                possible_moves += 1
                new_node = insert_at_node(self, self.value+1)
                move_balls(new_node, space)
                create_children(new_node, depth-1)
    if possible_moves == 0:
        print("Game Over!")

# Moves balls from a given move_from position, will play out the events until it lands in an empty pit or in the pot
def move_balls(node_in, move_from):
    # Handle simple errors
    if move_from < 0 or move_from > 13:
        print("Error, selected value is out of bounds!")
        return -1
    if move_from == 6 or move_from == 13:
        print("Error, cant move from player pits!")
        return -1
    if node_in.boardState[move_from] == 0:
        print("Error, you tried to move from empty pot")
        return -1
    if node_in.boardState[6] + node_in.boardState[13] == total_ball_count*12:
        print("Error, no balls left to move")
        return -1
    if (node_in.turn == 1 and move_from > 6) or (node_in.turn == 2 and move_from < 6):
        print("Error, you have to move from your side!")
        return -1

    # Update the last move
    node_in.last_move = move_from

    # Pick up balls and start moving
    currpos = move_from
    hand = node_in.boardState[move_from]
    node_in.boardState[move_from] = 0

    # Move until hand is empty
    while hand != 0:

        # Move 1 position
        currpos += 1

        # Skip the pots based on what turn is moving
        if node_in.turn == 1 and currpos == 13:
            currpos +=1
        if node_in.turn == 2 and currpos == 6:
            currpos +=1

        # Make sure we start from beginning
        if currpos > 13:
            currpos = 0

        # Drop a ball
        node_in.boardState[currpos] += 1
        hand -= 1

        # If we drop the last ball check if there's move than ball in that pit
        # we also make sure we don't pick up from the pots
        if hand == 0 and node_in.boardState[currpos] > 1 and not (currpos == 6 or currpos == 13):
            hand = node_in.boardState[currpos]
            node_in.boardState[currpos] = 0
    pl1_side= 0
    pl2_side= 0
    for i in range(0, 6):
        pl1_side += node_in.boardState[i]
    for i in range(7, 13):
        pl2_side += node_in.boardState[i]

    # Player 1 won
    if pl1_side == 0:
        node_in.done = True
        # Add balls from opponent side to pit
        node_in.boardState[6] += pl2_side
        # Remove the balls from opponent side
        for i in range(7, 13):
            node_in.boardState[i] = 0

    # Player 2 won
    if pl2_side == 0:
        node_in.done = True
        # Add balls from opponent side to pit
        node_in.boardState[13] += pl1_side
        for i in range(0, 6):
            node_in.boardState[i] = 0

    # If we end in our own store don't update
    if not(currpos == 6 or currpos == 13):
        node_in.turn += 1
        if node_in.turn > 2:
            node_in.turn = 1
    return node_in.turn

# Minimax, finds the best util value
# should maximize the value when the turn is 2
# should minimize when the turn is 1
def minimax(node_in, depth):
    # print("In minimax, depth = %d" % depth)
    if depth == 0:
        return calc_util(node_in)

    # If the node we visit is a done node, we return this node
    if node_in.done:
        node_in.best_node = node_in
        return calc_util(node_in)

    # If turn = 2 for the node we maximize
    if node_in.turn == 2:
        highest_so_far = -999999
        for each in node_in.children:
            val_from_child = minimax(each, depth-1)
            if val_from_child > highest_so_far:
                highest_so_far = val_from_child
                if each.best_node is None:
                    node_in.best_node = each
                else:
                    node_in.best_node = each.best_node
        best_fit = highest_so_far

    # If turn != 2 we minimize
    else:
        lowest_so_far = 999999
        for each in node_in.children:
            # Get minimax from each child
            val_from_child = minimax(each, depth-1)

            # If a lower value is available a minimizing node should pick this
            if val_from_child < lowest_so_far:
                lowest_so_far = val_from_child
                if each.best_node is None:
                    node_in.best_node = each
                else:
                    node_in.best_node = each.best_node
        best_fit = lowest_so_far
    # print("Best fit: %d" % best_fit)
    return best_fit



# Function traverses from the best node and up, then it returns the last nodes' move
def what_move(node_in):
    trav = node_in.best_node
    best_move = -1
    while trav is not node_in:
        best_move = trav.last_move
        trav = trav.parent

    return best_move


def check_if_done(node_in):
    if node_in.done:
        return node_in.turn
    else:
        return -1

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    total_ball_count = int(input("How many balls do you want to have in each pit? (4-6): "))
    # Limit input
    if total_ball_count > 6:
        total_ball_count = 6
    if total_ball_count < 4:
        total_ball_count = 4

    user_input = int(input("Play:\n1. Player vs AI\n2. Player vs Player\nSelect: "))
    if user_input == 1:
        play_with_ai = True
    else:
        play_with_ai = False

    if play_with_ai:
        ai_depth = int(input("How deep should the AI search? Keep in mind it gets harder to beat,\nand the thinking time gets higher the deeper you go (max: 9): "))
        # Limit input
        if ai_depth > 9:
            ai_depth = 9
        if ai_depth < 0:
            ai_depth = 1

        the_ai = CoolTree()                                             # Create agent


    board_node = Node() # Create a kalaha board

    if int(input("Who should go first? Player 1 or 2: ")) == 1:
        board_node.turn = 1
    else:
        board_node.turn = 2


    setup_start_board(board_node.boardState, total_ball_count)       # Make setup the board

    game_done = -1
    while game_done == -1:
        while board_node.turn == 1:
            print("Player 1 it's your turn!")
            print_state(board_node, "", True, False, False)  # Print the board
            move_from_this = int(input("What pit do you want to move from?:"))
            move_balls(board_node, move_from_this)

            # Check if the game is over
            game_done = check_if_done(board_node)
            if game_done != -1:
                break
        while board_node.turn == 2:
            print("Player 2/AI it's your turn!")
            if play_with_ai:
                print_state(board_node, "", True, False, False)  # Print the board
                print("AI finding the best move!")
                the_ai.head = copy.deepcopy(board_node)

                # Generate the tree we search in
                Node.total_nodes = 0
                create_children(the_ai.head, ai_depth)

                # Call the minimax, values found in the algorithm is stored in the nodes themselves
                minimax(the_ai.head, ai_depth)

                # Uncomment this to see the path the AI finds
                # print_parents(the_ai.head.best_node)

                # Find the move, based on what was found in the minimax
                move_this = what_move(the_ai.head)
                print("The best move that was found: %d" % move_this)
                # Print how many nodes are created
                print("%d nodes were searched\n" % Node.total_nodes)
                # Actually move it
                move_balls(board_node, move_this)
            else:
                print_state(board_node, "", True, False, False)  # Print the board
                move_from_this = int(input("What pit do you want to move from?:"))
                move_balls(board_node, move_from_this)

            # Check if the game is over
            game_done = check_if_done(board_node)
            if game_done != -1:
                break



    print("\n******************************************\nPlayer %d won!\n" % game_done)
    print_state(board_node, "", False, False, False)
    print("******************************************")

