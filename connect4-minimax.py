import numpy as np
import random

ROWS = 8
COLS = 8

PLAYER1 = 1
PLAYER2 = 2
OBSTACLE = 3
EMPTY = 0

def create_board():
    return np.full((ROWS, COLS), EMPTY)

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col): 
    return board[ROWS-1][col] == EMPTY and col < COLS #check if space above piece is available

def get_next_open_row(board, col):
    for r in range(ROWS):
        if board[r][col] == EMPTY:
            return r
        
def is_board_full(board):
    return np.all(board != EMPTY)

def winning_move(board, piece):
    # horizontal win
    for c in range(COLS-3):
        for r in range(ROWS):
            if board[r][c] == piece and all(board[r][c+i] == piece for i in range(1, 4)):
                return True
    # vertical win
    for c in range(COLS):
        for r in range(ROWS-3):
            if board[r][c] == piece and all(board[r+i][c] == piece for i in range(1, 4)):
                return True
    # diagnonal wins
    for c in range(COLS-3):
        for r in range(ROWS-3):
            if board[r][c] == piece and all(board[r+i][c+i] == piece for i in range(1, 4)):
                return True

    for c in range(COLS-3):
        for r in range(3, ROWS):
            if board[r][c] == piece and all(board[r-i][c+i] == piece for i in range(1, 4)):
                return True
    return False

def print_board(board):
    board = np.flip(board,0) #FLIPS THE BOARD 
    rows, cols = board.shape

    for i in range(rows):
        for j in range(cols):
            if board[i, j] == 1:
                print('\033[91m●\033[0m', end=' ')  #red
            elif board[i, j] == 2:
                print('\033[93m●\033[0m', end=' ')  #yellow
            elif board[i, j] == 3:
                print('X', end=' ')  
            else:
                print('○', end=' ')  
        print()  

def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = [c for c in range(COLS) if is_valid_location(board, c)]
    is_terminal = winning_move(board, PLAYER1) or winning_move(board, PLAYER2) or len(valid_locations) == 0
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, PLAYER1):
                return (None, 100000000000000)
            elif winning_move(board, PLAYER2):
                return (None, -100000000000000)
            else: 
                return (None, 0)
        else: #if not terminal case, return score relative to player
            current_player = PLAYER1 if maximizingPlayer else PLAYER2
            return (None, score_position(board, current_player))
    if maximizingPlayer:
        value = -np.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            # print_board(b_copy)
            # print()
            drop_piece(b_copy, row, col, PLAYER1)
            new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value
    else: # Minimizing player
        value = np.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            # print_board(b_copy)
            # print()
            drop_piece(b_copy, row, col, PLAYER2)
            new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if beta <= alpha:
                break
        return column, value

def score_position(board, piece):
    score = 0

    # score center columns higher
    center_array = [int(i) for i in list(board[:, COLS//2])]
    center_count = center_array.count(piece)
    score += center_count*3

    #horizontal
    for r in range(ROWS):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COLS-3):
            window = row_array[c:c+4]
            score += evaluate_window(window, piece)

    #vertical
    for c in range(COLS):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(ROWS-3):
            window = col_array[r:r+4]
            score += evaluate_window(window, piece)

    #diagonals
    for r in range(ROWS-3):
        for c in range(COLS-3):
            window = [board[r+i][c+i] for i in range(4)]
            score += evaluate_window(window, piece)

    for r in range(3, ROWS):
        for c in range(COLS-3):
            window = [board[r-i][c+i] for i in range(4)]
            score += evaluate_window(window, piece)

    return score

def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER1 if piece == PLAYER2 else PLAYER2
    empty_count = window.count(EMPTY)

    if window.count(piece) == 4:
        score += 100  # Win condition
    elif window.count(piece) == 3 and empty_count == 1:
        score += 5  # Potential win in one move
    elif window.count(piece) == 2 and empty_count == 2:
        score += 2 # two forms strong position

    if window.count(opp_piece) == 3 and empty_count == 1:
        score -= 4  #block opponent from winning (if possible)
    elif window.count(opp_piece) == 2 and empty_count == 2:
        score -= 2  #prevents opponent ideal positioning

    if window.count(piece) == 1 and empty_count == 3: #single pieces should spread out
        score += 1  

    return score

#search for optimal obstacle placement (random if no player has winning)
def place_obstacle(board):
    column_scores = []

    for col in range(COLS):
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, OBSTACLE)

            score_player1 = score_position(temp_board, PLAYER1)
            score_player2 = score_position(temp_board, PLAYER2)

            combined_score = -(abs(score_player1) + abs(score_player2)) #find worst score
            
            column_scores.append((combined_score, col, row))
    
    if column_scores:
        column_scores.sort(reverse=True, key=lambda x: x[0])  
        best_score, best_col, best_row = column_scores[0]
        drop_piece(board, best_row, best_col, OBSTACLE)
        #print(f"Obstacle placed at ({best_row}, {best_col}) with impact score {best_score}")


def play_game():
    board = create_board()
    turn = 0
    game_over = False
    print_board(board)

    while not game_over:
        if is_board_full(board):
            game_over = True
            print("It's a draw!")
            
        if turn != 0 and turn % random.randint(1,5) == 0:
            place_obstacle(board)
            print("Obstacle placed:")
            print_board(board)

        # decide whose turn it is
        current_player = PLAYER1 if turn % 2 == 0 else PLAYER2
        col, minimax_score = minimax(board, 5, -np.inf, np.inf, current_player == PLAYER1)

        player_color = f'\033[91mPlayer 1\033[0m' if turn%2 == 0 else '\033[93mPlayer 2\033[0m'

        print("=="*(ROWS+1))
        print(f"{player_color} moves")
        
        if col is not None:
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, current_player)
            if winning_move(board, current_player):
                game_over = True
                print(f"Player {current_player} wins!")

        print_board(board)
        turn += 1


play_game()