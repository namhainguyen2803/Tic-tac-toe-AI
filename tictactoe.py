from copy import deepcopy
import math
import random

X = "X"
O = "O"
EMPTY = None
INF = 1e5


class InvalidMovement(Exception):
    pass

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    init_board = initial_state()
    num_row = len(init_board)
    num_col = len(init_board[0])
    if board == init_board:
        return 'X'
    else:
        num_x = 0
        num_o = 0
        for i in range(num_row):
            for j in range(num_col):
                if board[i][j] == 'X':
                    num_x += 1
                elif board[i][j] == 'O':
                    num_o += 1
        if num_x > num_o:
            return 'O'
        elif num_x == num_o:
            return 'X'


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    num_row = len(board)
    num_col = len(board[0])

    res = list()
    for i in range(num_row):
        for j in range(num_col):
            if board[i][j] == EMPTY:
                res.append((i,j))
    return res


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    row = action[0]
    col = action[1]
    new_board = deepcopy(board)
    if board[row][col] == EMPTY:
        new_board[row][col] = player(board)
        return new_board
    else:
        raise InvalidMovement



def winner(board, level = 3):
    """
    Returns the winner of the game, if there is one.
    """
    num_row = len(board)
    num_col = len(board[0])

    for i in range(num_row):
        for j in range(num_col - level + 1):
            if board[i][j] == board[i][j+1] == board[i][j+2] and board[i][j] != None:
                print(i,j)
                print("1")
                return board[i][j]
            
            elif board[j][i] == board[j+1][i] == board[j+2][i] and board[j][i] != None:
                print(j,i)
                print("2")
                return board[j][i]
            
    for j in range(num_col - level + 1):
        if board[j][j] == board[j+1][j+1] == board[j+2][j+2] and board[j][j] != None:
            print(j,i)
            print("3")
            return board[j][j]
        elif board[j][num_col-j-1] == board[j+1][num_col-j-2] == board[j+2][num_col-j-3] and board[j][num_col-j-1] != None:
            print(j,num_col - j - 1)
            print("4")
            return board[j][num_col - j - 1]
    
    return None
            
            

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    
    if (winner(board) != None) or len(actions(board)) == 0:
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    result = winner(board)
    if result == None:
        return 0
    elif result == 'X':
        return 1
    else:
        return -1
    
    
def alpha_beta(board, depth = 0, alpha = -1e9, beta = 1e9):
    if terminal(board):
        return utility(board)
    else:
        possible_move = actions(board)
        if player(board) == "X":
            max_best_val = -1e9
            for move in possible_move:
                new_board = result(board, move)
                value = alpha_beta(new_board, depth + 1, alpha = alpha, beta = beta)
                max_best_val = max(value, max_best_val)
                alpha = max(alpha, max_best_val)
                if beta <= alpha:
                    break
            return max_best_val
        
        else:
            min_best_val = 1e9
            for move in possible_move:
                new_board = result(board, move)
                value = alpha_beta(new_board, depth + 1, alpha = alpha, beta = beta)
                min_best_val = min(value, min_best_val)
                beta = min(beta,min_best_val)
                if beta <= alpha:
                    break
            return min_best_val   
            
               
def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    turn = player(board)
    possible_move = actions(board)
    optimal_move = list()
    if turn == "X":
        num = -1e9
        for move in possible_move:
            optimal_score = alpha_beta(result(board, move))
            if num < optimal_score:
                num = optimal_score
                optimal_move = move
    else:
        num = 1e9
        for move in possible_move:
            optimal_score = alpha_beta(result(board, move))
            if num > optimal_score:
                num = optimal_score
                optimal_move = move
    return optimal_move
    

def max_value(board):
    v = -100
    if terminal(board):
        return utility(board)
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v

def min_value(board):
    v = 100
    if terminal(board):
        return utility(board)
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v