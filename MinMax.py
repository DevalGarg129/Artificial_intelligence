import math
import random

# ------------------------------------
#  Game Board Representation
# ------------------------------------
board = [" " for _ in range(9)]

def print_board():
    print()
    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print("---+---+---")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("---+---+---")
    print(f" {board[6]} | {board[7]} | {board[8]} ")
    print()

# ------------------------------------
# Win / Draw Checking
# ------------------------------------
def check_win(player):
    win_states = [
        (0,1,2), (3,4,5), (6,7,8),   # rows
        (0,3,6), (1,4,7), (2,5,8),   # cols
        (0,4,8), (2,4,6)             # diagonals
    ]
    return any(board[a] == board[b] == board[c] == player for a,b,c in win_states)

def check_draw():
    return " " not in board

# ------------------------------------
# Minimax Algorithm
# ------------------------------------
def minimax(depth, is_maximizing, alpha=float('-inf'), beta=float('inf'), use_pruning=False):
    if check_win("O"): return 1
    if check_win("X"): return -1
    if check_draw(): return 0

    if is_maximizing:
        best_score = -math.inf
        for i in range(9):
            if board[i] == " ":
                board[i] = "O"
                score = minimax(depth + 1, False, alpha, beta, use_pruning)
                board[i] = " "
                best_score = max(best_score, score)
                if use_pruning:
                    alpha = max(alpha, best_score)
                    if beta <= alpha: break
        return best_score
    else:
        best_score = +math.inf
        for i in range(9):
            if board[i] == " ":
                board[i] = "X"
                score = minimax(depth + 1, True, alpha, beta, use_pruning)
                board[i] = " "
                best_score = min(best_score, score)
                if use_pruning:
                    beta = min(beta, best_score)
                    if beta <= alpha: break
        return best_score

# ------------------------------------
# Computer Move (AI)
# ------------------------------------
def computer_move(difficulty="hard", use_pruning=False):
    if difficulty == "easy":
        move = random.choice([i for i in range(9) if board[i] == " "])
        board[move] = "O"
        return

    if difficulty == "medium":
        # 50/50 random + minimax
        if random.random() < 0.5:
            move = random.choice([i for i in range(9) if board[i] == " "])
            board[move] = "O"
            return

    best_score = -math.inf
    best_move = None

    for i in range(9):
        if board[i] == " ":
            board[i] = "O"
            score = minimax(0, False, use_pruning=use_pruning)
            board[i] = " "
            if score > best_score:
                best_score = score
                best_move = i

    board[best_move] = "O"

# ------------------------------------
# Human Move
# ------------------------------------
def player_move():
    while True:
        try:
            move = int(input("Enter your move (1-9): ")) - 1
            if move >= 0 and move <= 8 and board[move] == " ":
                board[move] = "X"
                break
            else:
                print("Invalid move.")
        except:
            print("Enter a valid number.")

# ------------------------------------
# Main Game Loop
# ------------------------------------
def play_game():
    print("Tic-Tac-Toe with Minimax AI")
    print("Difficulty Levels: easy | medium | hard")
    difficulty = input("Select difficulty: ").lower()
    if difficulty not in ["easy", "medium", "hard"]:
        difficulty = "hard"

    pruning = input("Enable Alpha-Beta Pruning (y/n)? ").lower() == "y"

    print_board()

    while True:
        player_move()
        print_board()
        if check_win("X"):
            print("You win!")
            break
        if check_draw():
            print("Draw!")
            break

        print("Computer thinking...")
        computer_move(difficulty, pruning)
        print_board()

        if check_win("O"):
            print("Computer wins!")
            break
        if check_draw():
            print("Draw!")
            break


play_game()
