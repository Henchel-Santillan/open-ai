from abc import ABC, abstractmethod
import math
import random


class Agent(ABC):
    
    def __init__(self, color, a_name):
        self.color = color
        self.a_name = a_name
        
    @abstractmethod
    def make_move(self, board, row, col, iseattype):
        pass
    
    
class HAgent(Agent):
    
    def __init__(self, color, a_name):
        super().__init__(color, a_name)
        
    def make_move(self, board, row, col, iseattype):
        print("\nMOVES:")
        moveset = board.cells[row][col].piece.valid_moves(board)
        
        if iseattype:
            moveset = moveset[1]
        
        for move in moveset:
            print("(" + str(move[0] + 1) + ", " + str(move[1] + 1) + ")")
        
        print()
        row2, col2 = int(input("\nROW: ")), int(input("COLUMN: "))
        
        while not board.cells[row][col].piece.in_moveset(moveset, row2, col2):
            print("\nENTER (ROW,COL) IN MOVES ONLY.")
            row, col = int(input("\nROW: ")), int(input("COLUMN: "))
        
        return row2, col2

#____________________________REFACTOR ALL AGENTS: make-move()___________________

#Refactor according to changes in game loop   
class RandAgent(Agent):
    
    def __init__(self, color, a_name):
        self.color = color
        self.a_name = a_name
    
    #remove row1, col1 from AI implementations and add row1, col1 to the signature
    #if iseattype is True, must use moveset only contains eats
    def make_move(self, board, iseattype):
        mnext = board.mnext(self.color)
        
        if not mnext:
            return -1, -1, -1, -1
        
        ridx1 = random.randint(0, len(mnext) - 1)
        row1, col1 = mnext[ridx1].row, mnext[ridx1].col
        
        moveset = board.cells[row1][col1].piece.valid_moves(board)
        
        if iseattype:
            moveset = moveset[1]
        
        ridx2 = random.randint(0, len(moveset) - 1)
        
        return row1, col1, moveset[ridx2][0], moveset[ridx2][1]
    
    
class MinimaxAgent(Agent):
    
    #ply can be used for difficulty 
    def __init__(self, color, a_name, ply):
        super().__init__(color, a_name)
        self.ply = ply
    
    def make_move(self, board, iseattype):
        pass


class PerfectAgent(Agent):
    
    def __init__(self, color, a_name):
        super().__init__(color, a_name)
        
    def make_move(self, board, iseattype):
        pass
        