from abc import ABC, abstractmethod
from enum import Enum, unique

import math
import random

from cfour.util import Board

@unique
class State(Enum):
    OPP = -1
    EMP = 0
    AI = 1

class Agent(ABC):
    
    def __init__(self, color, a_name):
        self.color = color
        self.a_name = a_name
        
    @abstractmethod
    def make_move(self, board):
        pass
    

class HAgent(Agent):
    
    def __init__(self, color, a_name):
        super().__init__(color, a_name)
        
    def make_move(self, board):
        moveset = board.valid_moves()
        
        print("MOVES\n")
        
        for move in moveset:
            print("(" + str(move[0] + 1) + ", " + str(move[1] + 1) + ")", end=" ")
        
        print()
        row, col = int(input("\nROW: ")), int(input("COLUMN: "))
        
        while not board.in_moveset(moveset, row - 1, col - 1):
            print("INPUT (ROW, COL) IN MOVES ONLY.")
            row, col = int(input("\nROW: ")), int(input("COLUMN: "))
            
        return row - 1, col - 1 
    

class RandAgent(Agent):
    
    def __init__(self, color, a_name):
        self.color = color
        self.a_name = a_name
        
    def make_move(self, board):
        moveset = board.valid_moves()
        idx = random.randint(0, len(moveset) - 1)
        
        return moveset[idx][0], moveset[idx][1]
    
#same as ab-pruned minimax
class ABMinimaxAgent(Agent):
    
    def __init__(self, color, a_name):
        super().__init__(color, a_name)
        
    def make_move(self, board):
        pass
    
    def eval_bitboard(self, bitboard, shift):
        temp_bitboard = bitboard & (bitboard >> shift)
        return temp_bitboard & (temp_bitboard >> 2 * shift)
    
    def winner(self, board, color):
        bitboard = board.to_bitboard(color)
        
        vshift, hshift, adshift, ddshift = 1, 7, 8, 6
        
        return (self.eval_bitboard(bitboard, vshift) or 
                self.eval_bitboard(bitboard, hshift) or 
                self.eval_bitboard(bitboard, adshift) or 
                self.eval_bitboard(bitboard, ddshift))
        
    def full(self, board):
        bitboard = board.to_bitboard()
        return not any()
        
    def abminimax(self, board, node, a, b, ismax):
        if self.winner(board, self.color):
            return State.AI
        
        if self.winner(board, self.color.opposite()):
            return State.OPP
        
        
            
        
        