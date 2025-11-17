import random
random.seed(109)

#############################################
# INITIAL IMPLEMENTATION (STUFF FROM HW6)
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

print("Player 1 wins:") 
print(p1_win)
print("Player 2 wins:")
print(p2_win)
print("Number of ties") 
print(ties)
print("Average number of turns per game:")
print(total_turns / games)


#############################################
# MIN MAX IMPLEMENTATION
##############################################






















#############################################
# GAME TREE IMPLEMENTATION
##############################################


# code for building a tree: for our game tree, each node is the state of the boad, key is board state
class Node:
    def __init__(self, key, p):
        self.key = key
        self.parent = p
        children = []

class Tree:
    
    def __init__(self, rootkey, depth):
        #create a new tree while setting root
        self.root = rootkey

    #this one might not be needed 
    def checkTree(self, key, parentKey, root):
        #Recursive function that searches through tree to find if parentKey exists
        # note that 'root' input is not necessarily the root of the tree ('self')
        # 'root' is just where to start looking for the right parentKey to add this new node
        if root == None:
            #if there is no root in tree
            return False
        if root.key == parentKey:
            if root.left_child == None or root.right_child == None:
                # the node 'root' is the parent you should add the new child node to
                return root 
            else:
                print("Parent has two children, node not added.")
                return False
        else:
            for child in root.getChildren():
                # check 'root' node's children if they are the parent you're looking for
                add_temp = self.checkTree(key, parentKey, child)
                if add_temp:
                    return add_temp

                
    #####################              
    # Your code for the add method goes here.
    #####################
    def add(self, key, parentKey):
        node = self.checkTree(key, parentKey,self.root)
        if node is not False:
            node.children.append(key)


    #need to modify
    def findNodeDelete(self, key, root):
        if root == None:
            return False
        if key == root.key:
            if root.left_child == None and root.right_child == None:
                if root.parent.left_child.key == key:
                    root.parent.left_child = None
                elif root.parent.right_child.key == key:
                    root.parent.right_child = None
                root = None
                return True
            else:
                print("Node not deleted, has children")
                return False
        else:
            for child in root.getChildren():
                delete_node = self.findNodeDelete(key, child)
                if delete_node:
                    return delete_node

    def delete(self, key):
        if self.root == None:
            self.root = Node(key, None, None, None)
        if key == self.root.key:
            if self.root.left_child == None and self.root.right_child == None:
                self.root = None
                return True
            else:
                print("Node not deleted, has children")
                return False
        else:
            for child in self.root.getChildren():
                delete_node = self.findNodeDelete(key, child)
                if delete_node:
                    return delete_node

        print("Parent not found." )
        return False
