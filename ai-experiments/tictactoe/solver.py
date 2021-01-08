import math
from enum import Enum, unique

@unique
class State(Enum):
    PLAYER = -10
    EMPTY = 0
    AI = 10
    
def player(board, first):    
    if (9 - len(valid_moves(board))) % 2 == 0 :
        return first

    return 'X' if first == 'O' else 'O'
    
def winner(board, first):
    cp = player(board, first)
    
    for x in range(3):
        if (board[0][x] == board[1][x] == board[2][x] or 
            board[x][0] == board[x][1] == board[x][2]):
            return cp
    
    if (board[0][0] == board[1][1] == board[2][2] or 
        board[0][2] == board[1][1] == board[2][0]):
        return cp
    
    return None

def full(board):
    return not any(cell == '' for row in board for cell in row)

def valid_moves(board):
    return [(r, c) for c in range(3) for r in range(3) if board[r][c] == '']

def minimax(board, node, ismax, first):
    if winner(board, first) is not None:
        if node == 'X':
            return State.AI.value
        else:
            return State.PLAYER.value
        
    if full(board):
        return State.EMPTY.value
    
    p = player(board, first)
    
    if ismax:
        score = -math.inf
        
        for move in valid_moves(board):
            board[move[0]][move[1]] = p
            score = minimax(board, board[move[0]][move[1]], False, first)
            board[move[0]][move[1]] = ""
            
        return score
    
    else:
        score = math.inf
        
        for move in valid_moves(board):
            board[move[0]][move[1]] = p
            score = minimax(board, board[move[0]][move[1]], True, first)
            board[move[0]][move[1]] = ""
            
        return score
        
def abminimax(board, node, a, b, ismax, first):
    if winner(board, first) is not None:
        if node == 'X':
            return State.AI.value
        else:
            return State.PLAYER.value
        
    if full(board):
        return State.EMPTY.value
        
    p = player(board, first)
        
    if ismax:
        score = -math.inf
        
        for move in valid_moves(board):
            board[move[0]][move[1]] = p
            score = max(score, abminimax(board, board[move[0]][move[1]], a, b, False, first))
            board[move[0]][move[1]] = ''
            
            a = max(a, score)

            if a >= b:
                break
            
        return score
    
    else:
        score = math.inf
        
        for move in valid_moves(board):
            board[move[0]][move[1]] = player
            score = min(score, abminimax(board, board[move[0]][move[1]], a, b, True, first))
            board[move[0]][move[1]] = ''
            b = min(b, score)
            
            if b <= a:
                break
            
        return score

def mm_best_move(board, first):
    best_score = -math.inf
    best_move = (-1, -1)
    
    p = player(board, first)
    
    for move in valid_moves(board):
        board[move[0]][move[1]] = p
        score = minimax(board, board[move[0]][move[1]], True, first)  
        board[move[0]][move[1]] = ''
        
        if score > best_score:
            best_score = score
            best_move = move
    
    return best_move

def ab_best_move(board, first):
    best_score = -math.inf
    best_move = (-1, -1)
    
    p = player(board, first)
    
    for move in valid_moves(board):
        board[move[0]][move[1]] = p
        score = abminimax(board, board[move[0]][move[1]], -math.inf, math.inf, True, first)  
        board[move[0]][move[1]] = ''
        
        if score > best_score:
            best_score = score
            best_move = move
    
    return best_move

def main():
    board = [
        ['X', 'O', 'X'],
        ['', 'O', 'X'],
        ['', '', '']
        ]
    
    print(mm_best_move(board, 'X'))
    
main()
    