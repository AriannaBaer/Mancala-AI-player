import random
random.seed(109)

class Mancala:
    def __init__(self, pits_per_player=6, stones_per_pit=4):
        self.pits_per_player = pits_per_player
        self.board = [stones_per_pit] * ((pits_per_player + 1) * 2)
        self.players = 2
        self.current_player = 1
        self.moves = []
        self.p1_pits_index = [0, self.pits_per_player - 1]
        self.p1_mancala_index = self.pits_per_player
        self.p2_pits_index = [self.pits_per_player + 1, len(self.board) - 2]
        self.p2_mancala_index = len(self.board) - 1
        self.game_over = False
        # zero the stores
        self.board[self.p1_mancala_index] = 0
        self.board[self.p2_mancala_index] = 0

    def valid_move(self, pit):
        if pit is None:
            return False
        if not (1 <= pit <= self.pits_per_player):
            return False

        if self.current_player == 1:
            start, end = self.p1_pits_index
            idx = start + (pit - 1)
        else:
            start, end = self.p2_pits_index
            idx = end - (pit - 1)

        if not (start <= idx <= end):
            return False
        if self.board[idx] <= 0:
            return False
        return True

    def random_move_generator(self):
        if self.current_player == 1:
            start, end = self.p1_pits_index
            to_idx = lambda pit_num: start + (pit_num - 1)
        else:
            start, end = self.p2_pits_index
            to_idx = lambda pit_num: end - (pit_num - 1)

        options = [p for p in range(1, self.pits_per_player + 1)
                   if self.board[to_idx(p)] > 0]
        if not options:
            return None
        return random.choice(options)

    def play(self, pit):
        if self.game_over:
            return False
        if not self.valid_move(pit):
            return False

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

        idx = (p1_start + (pit - 1)) if player == 1 else (p2_end - (pit - 1))
        stones = b[idx]
        b[idx] = 0

        # sow stones counterclockwise, skip opponent's store
        while stones > 0:
            idx = (idx + 1) % total_len
            if idx == opp_store:
                continue
            b[idx] += 1
            stones -= 1

        # capture if last stone lands in own empty pit
        if player == 1 and p1_start <= idx <= p1_end and b[idx] == 1:
            opp = 2 * n - idx
            captured = b[opp]
            if captured > 0:
                b[my_store] += captured + 1
                b[idx] = 0
                b[opp] = 0
        elif player == 2 and p2_start <= idx <= p2_end and b[idx] == 1:
            opp = 2 * n - idx
            captured = b[opp]
            if captured > 0:
                b[my_store] += captured + 1
                b[idx] = 0
                b[opp] = 0

        # extra turn if last stone in own store
        extra_turn = (idx == my_store)

        # check game over (one side empty → sweep)
        self.winning_eval()
        if not self.game_over and not extra_turn:
            self.current_player = 2 if player == 1 else 1

        return self.board

    def winning_eval(self):
        b = self.board
        p1_start, p1_end = self.p1_pits_index
        p2_start, p2_end = self.p2_pits_index
        p1_store_idx = self.p1_mancala_index
        p2_store_idx = self.p2_mancala_index

        p1_empty = all(b[i] == 0 for i in range(p1_start, p1_end + 1))
        p2_empty = all(b[j] == 0 for j in range(p2_start, p2_end + 1))

        if not (p1_empty or p2_empty):
            self.game_over = False
            return False

        if p1_empty and not p2_empty:
            rem2 = sum(b[j] for j in range(p2_start, p2_end + 1))
            for j in range(p2_start, p2_end + 1):
                b[j] = 0
            b[p2_store_idx] += rem2
        elif p2_empty and not p1_empty:
            rem1 = sum(b[i] for i in range(p1_start, p1_end + 1))
            for i in range(p1_start, p1_end + 1):
                b[i] = 0
            b[p1_store_idx] += rem1
        # if both empty, nothing to sweep

        p1_final = b[p1_store_idx]
        p2_final = b[p2_store_idx]
        self.final_scores = (p1_final, p2_final)
        self.game_over = True
        self.winner = 1 if p1_final > p2_final else 2 if p2_final > p1_final else 0
        return True


# ---- Simulate 100 games with both players random ----
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
