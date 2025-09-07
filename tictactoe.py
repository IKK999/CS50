"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


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
    Xs = 0
    Os = 0
    for row in board:
        for cell in row:
            if cell == X:
                Xs += 1
            elif cell == O:
                Os += 1
    if Xs == Os:
        return X
    elif Xs > Os:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    options = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                options.append((i, j))
    return options


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if board[action[0]][action[1]] != EMPTY:
        raise Exception("Invalid move")
    else:
        board[action[0]][action[1]] = player(board)
        return board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    CURP = X
    if board[0][0] == CURP and board[0][1] == CURP and board[0][2] == CURP:
        return CURP
    if board[1][0] == CURP and board[1][1] == CURP and board[1][2] == CURP:
        return CURP
    if board[2][0] == CURP and board[2][1] == CURP and board[2][2] == CURP:
        return CURP
    if board[0][0] == CURP and board[1][0] == CURP and board[2][0] == CURP:
        return CURP
    if board[0][1] == CURP and board[1][1] == CURP and board[2][1] == CURP:
        return CURP
    if board[0][2] == CURP and board[1][2] == CURP and board[2][2] == CURP:
        return CURP
    if board[0][0] == CURP and board[1][1] == CURP and board[2][2] == CURP:
        return CURP
    if board[0][2] == CURP and board[1][1] == CURP and board[2][0] == CURP:
        return CURP
    
    CURP = O
    if board[0][0] == CURP and board[0][1] == CURP and board[0][2] == CURP:
        return CURP
    if board[1][0] == CURP and board[1][1] == CURP and board[1][2] == CURP:
        return CURP
    if board[2][0] == CURP and board[2][1] == CURP and board[2][2] == CURP:
        return CURP
    if board[0][0] == CURP and board[1][0] == CURP and board[2][0] == CURP:
        return CURP
    if board[0][1] == CURP and board[1][1] == CURP and board[2][1] == CURP:
        return CURP
    if board[0][2] == CURP and board[1][2] == CURP and board[2][2] == CURP:
        return CURP
    if board[0][0] == CURP and board[1][1] == CURP and board[2][2] == CURP:
        return CURP
    if board[0][2] == CURP and board[1][1] == CURP and board[2][0] == CURP:
        return CURP
    
    CURP = EMPTY
    return CURP


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    game_winner = winner(board)
    if game_winner == X or game_winner == O:
        return True
    else:
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    return False
        return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    game_winner = winner(board)
    if game_winner == X:
        return 1
    elif game_winner == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    def max_value(board):
        if terminal(board):
            return utility(board)
        v = -float('inf')
        for action in actions(board):
            v = max(v, min_value(result(board, action)))
            board[action[0]][action[1]] = EMPTY
        return v
    
    def min_value(board):
        if terminal(board):
            return utility(board)
        v = float('inf')
        for action in actions(board):
            v = min(v, max_value(result(board, action)))
            board[action[0]][action[1]] = EMPTY
        return v

    if terminal(board):
        return None
    
    current_player = player(board)
    best_action = None
    
    if current_player == X: 
        best_value = -float('inf')
        for action in actions(board):
            new_board = result(board, action)
            value = min_value(new_board)
            if value > best_value:
                best_value = value
                best_action = action
            board[action[0]][action[1]] = EMPTY
    else: 
        best_value = float('inf')
        for action in actions(board):
            new_board = result(board, action)
            value = max_value(new_board)
            if value < best_value:
                best_value = value
                best_action = action
            board[action[0]][action[1]] = EMPTY
    
    return best_action