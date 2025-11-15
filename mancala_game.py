import random
random.seed(109)

# for the game tree 
import copy


#############################################
# INITIAL IMPLEMENTATION (STUFF FROM HW6)
# #1-2 on the write-up
##############################################

class Mancala:
    def __init__(self, pits_per_player=6, stones_per_pit = 4):
        """
        The constructor for the Mancala class defines several instance variables:

        pits_per_player: This variable stores the number of pits each player has.
        stones_per_pit: It represents the number of stones each pit contains at the start of any game.
        board: This data structure is responsible for managing the Mancala board.
        current_player: This variable takes the value 1 or 2, as it's a two-player game, indicating which player's turn it is.
        moves: This is a list used to store the moves made by each player. It's structured in the format (current_player, chosen_pit).
        p1_pits_index: A list containing two elements representing the start and end indices of player 1's pits in the board data structure.
        p2_pits_index: Similar to p1_pits_index, it contains the start and end indices for player 2's pits on the board.
        p1_mancala_index and p2_mancala_index: These variables hold the indices of the Mancala pits on the board for players 1 and 2, respectively.
        """
        self.pits_per_player = pits_per_player
        self.board = [stones_per_pit] * ((pits_per_player+1) * 2)  # Initialize each pit with stones_per_pit number of stones 
        self.players = 2
        self.current_player = 1
        self.moves = []
        self.p1_pits_index = [0, self.pits_per_player-1]
        self.p1_mancala_index = self.pits_per_player
        self.p2_pits_index = [self.pits_per_player+1, len(self.board)-1-1]
        self.p2_mancala_index = len(self.board)-1
        
        # Zeroing the Mancala for both players
        self.board[self.p1_mancala_index] = 0
        self.board[self.p2_mancala_index] = 0

        #We added this portion for the random vs random player simulation
        self.game_over = False
        self.winner = 0
        self.final_scores = (0, 0)

    def display_board(self):
        """
        Displays the board in a user-friendly format
        """
        player_1_pits = self.board[self.p1_pits_index[0]: self.p1_pits_index[1]+1]
        player_1_mancala = self.board[self.p1_mancala_index]
        player_2_pits = self.board[self.p2_pits_index[0]: self.p2_pits_index[1]+1]
        player_2_mancala = self.board[self.p2_mancala_index]

        print('P1               P2')
        print('     ____{}____     '.format(player_2_mancala))
        for i in range(self.pits_per_player):
            if i == self.pits_per_player - 1:
                print('{} -> |_{}_|_{}_| <- {}'.format(i+1, player_1_pits[i], 
                        player_2_pits[-(i+1)], self.pits_per_player - i))
            else:    
                print('{} -> | {} | {} | <- {}'.format(i+1, player_1_pits[i], 
                        player_2_pits[-(i+1)], self.pits_per_player - i))
            
        print('         {}         '.format(player_1_mancala))
        turn = 'P1' if self.current_player == 1 else 'P2'
        print('Turn: ' + turn)
        
    def valid_move(self, pit):
        """
        Function to check if the pit chosen by the current_player is a valid move.
        """
        # guard against None or out-of-range pit numbers
        if pit is None or not (1 <= pit <= self.pits_per_player):
            return False

        if self.current_player == 1:
            start, end = self.p1_pits_index          
            idx = start + (pit - 1)                  
        else:
            start, end = self.p2_pits_index          
            idx = end - (pit - 1)                    

        #returns false if pit chosen was not on your side 
        if not (start <= idx <= end):
            return False
        
        #returns false if pit is empty
        if self.board[idx] <= 0:
            return False

        return True
        
    def random_move_generator(self):
        """
        Function to generate random valid moves with non-empty pits for the random player
        """
        
        # figure out which side we're on
        if self.current_player == 1:
            start, end = self.p1_pits_index 
            # mapping for P1 pits matches valid_move/play
            to_idx = lambda pit_num: start + (pit_num - 1)
        else:
            start, end = self.p2_pits_index
            # mapping for P2 pits matches valid_move/play
            to_idx = lambda pit_num: end - (pit_num - 1)

        
        options = []
        for pit_num in range(1, self.pits_per_player + 1):
            idx = to_idx(pit_num)        
            if self.board[idx] > 0:
                options.append(pit_num)

        if not options:
            return None  

        choice = random.choice(options)
        return choice
        
        pass
    
    def play(self, pit):
        """
        This function simulates a single move made by a specific player using their selected pit. It primarily performs three tasks:
        1. It checks if the chosen pit is a valid move for the current player. If not, it prints "INVALID MOVE" and takes no action.
        2. It verifies if the game board has already reached a winning state. If so, it prints "GAME OVER" and takes no further action.
        3. After passing the above two checks, it proceeds to distribute the stones according to the specified Mancala rules.

        Finally, the function then switches the current player, allowing the other player to take their turn.
        """
        #step 1
        if self.valid_move(pit) == False:
            #print("INVALID MOVE")
            return False

        #step 2
        if self.winning_eval() == True:
            #print("GAME OVER")
            return False

        #step 3
        #how i am going to approach this:
            #Check number of stones and make a loop that deincrements and distributes one in every pit until number of stones is 0
            #maybe make two loops one that increments the pit and checks that the pit is not the opposing players mancala pit and maybe one loop that deincrements number of stones if pit is applicable?
        b = self.board
        n = self.pits_per_player
        p1_start, p1_end = self.p1_pits_index
        p2_start, p2_end = self.p2_pits_index
        p1_store = self.p1_mancala_index
        p2_store = self.p2_mancala_index
        total_len = len(b)

        player = self.current_player
        my_store = p1_store if player == 1 else p2_store
        opp_store = p2_store if player == 1 else p1_store


        #to match the expected image
        #commenting out so we can just see random stuff
        #print(f"Player {player} chose pit: {pit}")   
        self.moves.append((player, pit))     
        
        if player == 1:
            idx = p1_start + (pit - 1)
        else:
            idx = p2_end - (pit - 1)


        #pick up stones/set pit chosen to 0
        stones = b[idx]
        b[idx] = 0

        #move stones one by one counterclockwise 
        #we mod by length to make sure that stones wrap around the board once you hit the last pit
        while stones > 0:
            idx = (idx + 1) % total_len 
            if idx == opp_store:
                continue
            b[idx] += 1
            stones -= 1

        #capture rule
        # if players pit is on players side and there is only one stone in that pit (aka last stone was in an empty pit)
        if player == 1 and p1_start <= idx <= p1_end and b[idx] == 1:
            #find the opposite 
            # take 2 times total number of pits per player to get total pits then subtract the index
            opp = 2 * n - idx
            captured = b[opp]
            if captured > 0:
                b[my_store] += captured + 1
                #now set both stones total to 0
                b[idx] = 0
                b[opp] = 0
        #same code but for player 2
        elif player == 2 and p2_start <= idx <= p2_end and b[idx] == 1:
            opp = 2 * n - idx
            captured = b[opp]
            if captured > 0:
                b[my_store] += captured + 1
                b[idx] = 0
                b[opp] = 0
            
        self.current_player = 2 if player == 1 else 1
        return self.board
    
    def winning_eval(self):
        """
        Function to verify if the game board has reached the winning state.
        Hint: If either of the players' pits are all empty, then it is considered a winning state.
        """
        #define all variables
        b = self.board
        p1_start, p1_end = self.p1_pits_index
        p2_start, p2_end = self.p2_pits_index
        p1_store_idx = self.p1_mancala_index
        p2_store_idx = self.p2_mancala_index

        #check if p1s pits are empty
        p1_empty = True
        i = p1_start
        while i <= p1_end:
            if b[i] != 0:
                p1_empty = False
                break
            i += 1

        #check if p2s pits are empty
        p2_empty = True
        j = p2_start
        while j <= p2_end:
            if b[j] != 0:
                p2_empty = False
                break
            j += 1

        #in the case neither are empty return false
        if not (p1_empty or p2_empty):
            self.game_over = False
            return False

        #calculate the total number of stones
        TOTAL = 0
        k = 0
        while k < len(b):
            TOTAL += b[k]
            k += 1

        if p1_empty and p2_empty:
            # both sides already empty; nothing to sweep
            p1_final = b[p1_store_idx]
            p2_final = b[p2_store_idx]

        elif p1_empty:
            # sweep P2's remaining stones into P2's mancala
            rem2 = 0
            j = p2_start
            while j <= p2_end:
                rem2 += b[j]
                b[j] = 0
                j += 1
            b[p2_store_idx] += rem2

            p1_final = b[p1_store_idx]
            p2_final = b[p2_store_idx]

        else:
            # (only P2 empty) sweep P1's remaining stones into P1's mancala
            rem1 = 0
            i = p1_start
            while i <= p1_end:
                rem1 += b[i]
                b[i] = 0
                i += 1
            b[p1_store_idx] += rem1

            p1_final = b[p1_store_idx]
            p2_final = b[p2_store_idx]

        self.final_scores = (p1_final, p2_final)
        self.game_over = True

        if p1_final > p2_final:
            self.winner = 1
        elif p2_final > p1_final:
            self.winner = 2
        else:
            self.winner = 0  # tie

        return True






#############################################
#CODE FOR INTERMEDIATE EVAL (RANDOM vs RANDOM PLAYER SIM)
# #3 on the writeup
##############################################

games = 100
p1_win = p2_win = ties = 0
total_turns = 0
random.seed(109)

for _ in range(games):
    game = Mancala()
    turns = 0
    while not game.game_over:
        move = game.random_move_generator()
        if move is None:
            # no legal move for current player → finalize/sweep and end
            game.winning_eval()
            break
        game.play(move)
        turns += 1

    if game.winner == 1:
        p1_win += 1
    elif game.winner == 2:
        p2_win += 1
    else:
        ties += 1
    total_turns += turns

print("Random vs Random sim results:")
print("Player 1 wins:", p1_win)
print("Player 2 wins:", p2_win)
print("Ties:", ties)
print("Player 1 win percentage:", p1_win / games * 100, "%")
print("Average number of turns per game:", total_turns / games)







#############################################
# MIN MAX IMPLEMENTATION
##############################################
# goal/ what to implement:
    #First look ahead some number of piles (this is depth)
        #Then at the bottom/leaf nodes assign a value using the utility function to the state
            #Then minman works back up the tree
                #Max levels pick the max child value
                    #min levels pick the min child value
                        #once we hit the root, the move that leads to the highest max value is chosen


#start with the helper functions
def legal_moves(game):
    """
    returns the total list of moves so we dont have to make a loop like we did in random_move_generator
    and when building the tree
    """
    return [pit for pit in range(1, game.pits_per_player + 1) if game.valid_move(pit)]


def evaluate_utility(game, max_player):
    """
    does the utility function for us
    Utility = stones in Max's mancala - stones in Min's mancala.
    """
    p1_store = game.p1_mancala_index
    p2_store = game.p2_mancala_index

    #if AI player is 1 or 2
    if max_player == 1:
        return game.board[p1_store] - game.board[p2_store]
    else:
        return game.board[p2_store] - game.board[p1_store]
    

#logic of the recursive function/basically what i am trying to do
    #Find all legal moves for player
        #base case is if game is already over/depth = 0
            #if base case just evaluate utility function
        #if max player == current player
            #copy the game, use play function, recurse, returns the maximum of those values
        #same idea if not max player but the minimum of those values

def minimax_value(game, depth, max_player):
    """
    Returns the number the utility function calculated
    """
    #call our helper function for a list of legal moves
    moves = legal_moves(game)

    #Base cases: when game is already over, no legal moves, or depth = 0
    if game.game_over:
        return evaluate_utility(game, max_player)

    if not moves:
        terminal_copy = copy.deepcopy(game)
        terminal_copy.winning_eval()
        return evaluate_utility(terminal_copy, max_player)

    if depth == 0:
        return evaluate_utility(game, max_player)


    is_max_turn = (game.current_player == max_player)


    if is_max_turn:
        #chooses the move with highest value
        #we assign the value to negative infinity so that any real move value will be higher
        best_val = float('-inf')
        for move in moves:
            child_game = copy.deepcopy(game)
            child_game.play(move)
            #use recursion here
            val = minimax_value(child_game, depth - 1, max_player)
            if val > best_val:
                best_val = val
        return best_val
    else:
        #if player is min
        #we want the choice with the lowest value so we set best_val to the highest possible value which is infinity
        best_val = float('inf')
        for move in moves:
            child_game = copy.deepcopy(game)
            child_game.play(move)
            val = minimax_value(child_game, depth - 1, max_player)
            if val < best_val:
                best_val = val
        return best_val







##############################################
# AI MIN MAX VS RANDOM PLAYER SIM
# 4-5 on the project write up
##############################################

#What percentage of games does each player (AI or random) win?
#On average, how many moves does it take to win?

#Play 100 games with the random player against the minimax AI player at a depth of 5 plies

def minimax_ai_move(game, depth):
    """
    Choose the best move for the *current player* in 'game' using minimax.
    returns a pit number, or none if no legal moves.
    """
    max_player = game.current_player
    moves = legal_moves(game)

    if not moves:
        return None  

    best_val = float('-inf')
    best_moves = []

    for move in moves:
        #simulate this move
        child_game = copy.deepcopy(game)
        child_game.play(move)

        #look ahead from the resulting state
        val = minimax_value(child_game, depth - 1, max_player)

        #update best move list
        if val > best_val:
            best_val = val
            best_moves = [move]
        elif val == best_val:
            best_moves.append(move)

    #if multiple moves tie, pick one randomly
    return random.choice(best_moves)


#Code for the simulation very similar to RANDOM VS RANDOM 
games = 100
ai_wins = 0
random_wins = 0
ties = 0
total_turns = 0

for _ in range(games):
    game = Mancala()
    turns = 0

    #set max player to 1
    ai_player = 1

    while not game.game_over:
        if game.current_player == ai_player:
            move = minimax_ai_move(game, depth=5)
        else:
            move = game.random_move_generator()

        if move is None:
            game.winning_eval()
            break

        game.play(move)
        turns += 1

    #add up the results
    if game.winner == ai_player:
        ai_wins += 1
    elif game.winner == 0:
        ties += 1
    else:
        random_wins += 1

    total_turns += turns

print("MinMax sim results:")
print("Minimax AI wins:", ai_wins)
print("Random wins:", random_wins)
print("Ties:", ties)
print("AI win percentage:", ai_wins / games * 100, "%")
print("Average number of turns per game:", total_turns / games)









#############################################
# Alpha BETA IMPLEMENTATION
# #6 on the write up
#############################################

# what is alpha beta pruning:
    #same idea as minmax except with one caveat
    #When evaluating a branch,
    #if you discover that:
        #Max already has a move ≥ some value (alpha) AND Min can force a value ≤ some value (beta)
        #Then some branches will NEVER affect the final answer.
        #so you stop exploring them aka you prune them.


#basically min max but with these two new parameters
#alpha = “best value MAX can guarantee so far”
#beta = “best value MIN can guarantee so far”

def alphabeta_value(game, depth, alpha, beta, max_player):
    """
    copied same function from minmax but changed up the parameters and added a couple lines
    """
    #helper func
    moves = legal_moves(game)

   #Base cases: when game is already over, no legal moves, or depth = 0
    if game.game_over:
        return evaluate_utility(game, max_player)

    if not moves:
        terminal_copy = copy.deepcopy(game)
        terminal_copy.winning_eval()
        return evaluate_utility(terminal_copy, max_player)

    if depth == 0:
        return evaluate_utility(game, max_player)

    

    is_max_turn = (game.current_player == max_player)

    if is_max_turn:
        value = float('-inf')
        for move in moves:
            child = copy.deepcopy(game)
            child.play(move)

            #added/ different from minmax
            value = max(value,
                        alphabeta_value(child, depth - 1, alpha, beta, max_player))

            alpha = max(alpha, value)

            #this part is added
            if beta <= alpha:
                break

        return value

    else:
        value = float('inf')
        for move in moves:
            child = copy.deepcopy(game)
            child.play(move)

            #same thing as above/ the two-ish lines added/ different from min max
            value = min(value,
                        alphabeta_value(child, depth - 1, alpha, beta, max_player))

            beta = min(beta, value)

            # prune:
            if beta <= alpha:
                break

        return value



###############################################
# AI ALPHA BETA VS RANDOM PLAYER SIM
# 7-8 on the project write up
###############################################

#The move selector necessary for the random sim/basically same as minmax selector

def alphabeta_ai_move(game, depth):
    max_player = game.current_player
    moves = legal_moves(game)

    if not moves:
        return None

    best_val = float('-inf')
    best_moves = []

    alpha = float('-inf')
    beta = float('inf')

    for move in moves:
        child = copy.deepcopy(game)
        child.play(move)

        val = alphabeta_value(child, depth - 1, alpha, beta, max_player)

        # track best move(s)
        if val > best_val:
            best_val = val
            best_moves = [move]
        elif val == best_val:
            best_moves.append(move)

        #update alpha at the root- this is different then the minmax
        alpha = max(alpha, val)

    return random.choice(best_moves)



##################
# DEPTH 5 CODE (7)
games = 100
ai_wins = 0
random_wins = 0
ties = 0
total_turns = 0


for _ in range(games):
    game = Mancala()
    turns = 0
    ai_player = 1 

    while not game.game_over:
        if game.current_player == ai_player:
            move = alphabeta_ai_move(game, depth=5)
        else:
            move = game.random_move_generator()

        if move is None:
            game.winning_eval()
            break

        game.play(move)
        turns += 1

    if game.winner == ai_player:
        ai_wins += 1
    elif game.winner == 0:
        ties += 1
    else:
        random_wins += 1

    total_turns += turns

print("Alpha-Beta sim results (depth 5):")
print("Alpha-Beta AI wins:", ai_wins)
print("Random wins:", random_wins)
print("Ties:", ties)
print("AI win percentage:", ai_wins / games * 100, "%")
print("Average number of turns per game:", total_turns / games)


#########################
# DEPTH 10 CODE (8)
games = 100
ai_wins = 0
random_wins = 0
ties = 0
total_turns = 0

random.seed(109)

for _ in range(games):
    game = Mancala()
    turns = 0
    ai_player = 1  # Alpha-Beta AI is Player 1

    while not game.game_over:
        if game.current_player == ai_player:
            move = alphabeta_ai_move(game, depth=10)
        else:
            move = game.random_move_generator()

        if move is None:
            game.winning_eval()
            break

        game.play(move)
        turns += 1

    if game.winner == ai_player:
        ai_wins += 1
    elif game.winner == 0:
        ties += 1
    else:
        random_wins += 1

    total_turns += turns

print("Alpha-Beta sim results (depth 10):")
print("Alpha-Beta AI wins:", ai_wins)
print("Random wins:", random_wins)
print("Ties:", ties)
print("AI win percentage:", ai_wins / games * 100, "%")
print("Average number of turns per game:", total_turns / games)





#############################################
# GAME TREE IMPLEMENTATION
##############################################
# For our game tree, each node will store:
# - a Mancala game state (board + current_player, etc.)
# - a reference to its parent
# - the move (pit number) that led to this state from the parent
# - a list of children



#logic i used:
#build_tree(node, depth):

    #If depth is 0 → stop expanding
    #Else:
    #Look at the node’s game state
    #Generate legal pit moves for the current player
    #If no moves → stop (leaf)
    #For each move:
    #Deep copy the game state
    #Play that move on the copy (so board + current_player update exactly as in your game code)
    #Wrap the new state in a Node.
    #Attach to node.children.
    #Recurse with depth-1.


class Node:
    def __init__(self, game_state, parent=None, move=None):
        """
        game_state: a Mancala object representing this position
        parent: parent Node in the tree
        move: the pit  played from the parent to reach this node
        """
        self.state = game_state
        self.parent = parent
        self.move = move
        self.children = []

class Tree:
    
    def __init__(self, root_state):
        self.root = Node(root_state)

    def build_tree(self, node, depth):
        """
        recursively build the game tree starting from 'node' down to 'depth' plies.
        doesn't  modify the original Mancala
        because we deep-copy the game state at each child.
        """
        if depth == 0:
            return

        game = node.state

        #generate all legal moves (pits 1..pits_per_player)
        #we create a loop here much like we did in our random moves function
        moves = []
        for pit in range(1, game.pits_per_player + 1):
            if game.valid_move(pit):
                moves.append(pit)

        #no legal moves means this is a leaf node
        if not moves:
            return

        #for each legal move, create a child node with the resulting game state
        for pit in moves:
            #deep copy the current game so we don't overwrite this node's state
            next_game = copy.deepcopy(game)
            next_game.play(pit)  # applies the move and switches current_player

            child = Node(next_game, parent=node, move=pit)
            node.children.append(child)

            #recurse down one level
            self.build_tree(child, depth - 1)



#######################################
# TEST CASES TO CHECK IF TREE IS WORKING
########################################

# if correct output will be:
##     Number of children at root: 6
##     Moves from root: [1, 2, 3, 4, 5, 6]



#start from a fresh game
root_game = Mancala()

#create a tree with that as the root state
game_tree = Tree(copy.deepcopy(root_game))

#build the tree to depth 2 plies (you can change 2 to other small numbers)
game_tree.build_tree(game_tree.root, depth=2)

#how many children does the root have?
print("test cases that game tree is running properly")
print("Number of children at root:", len(game_tree.root.children))
print("Moves from root:", [child.move for child in game_tree.root.children])