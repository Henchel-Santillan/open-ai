from enum import Enum, unique
from abc import ABC, abstractmethod


@unique
class Identity(Enum):
    PAWN = "p"
    ROOK = "R"
    KNIGHT = "N"
    BISHOP = "B"
    QUEEN = "Q"
    KING = "K"
    
    @classmethod
    def values(cls):
        return [cls.PAWN, cls.ROOK, cls.KNIGHT, cls.BISHOP, cls.QUEEN, cls.KING]
    

@unique
class Color(Enum):
    BLACK = "B"
    WHITE = "W"
    
    @classmethod
    def values(cls):
        return [cls.BLACK, cls.WHITE]
    
    def opposite(self):
        return Color.BLACK if self is Color.WHITE else Color.WHITE
    

@unique
class Rule(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)
    UPLEFT = (-1, -1)
    UPRIGHT = (-1, 1)
    DOWNLEFT = (1, -1)
    DOWNRIGHT = (1, 1)
    
    @classmethod
    def values(cls):
        return [cls.UP, cls.DOWN, cls.LEFT, cls.RIGHT, 
                cls.UPLEFT, cls.UPRIGHT, cls.DOWNLEFT, cls.DOWNRIGHT]
    

#______________CAN INIT PIECES WITH STARTING POSITIONS_________________
class Piece(ABC):
    
    def __init__(self, row, col, color, identity):
        self.row, self.col = row, col
        self.color = color
        self.identity = identity
        
    def __str__(self):
        return self.color.value + self.identity.value
    
    def uci(self):
        if isinstance(self, Pawn):
            return ""
        return self.identity.value
    
    def update(self, row, col):
        self.row, self.col = row, col
    
    @abstractmethod
    def moveset(self, board):
        pass
    

class StrafingPiece(Piece):

    def __init__(self, row, col, color, identity):
        super().__init__(row, col, color, identity)
        #Upper and lower direction bounds
        self._upper, self._lower = -1, -1
        
    def moveset(self, board):
        moveset = []
        
        for x in range(self._upper, self._lower):
            rule = Rule.values()[x]
            row_n, col_n = self.row + rule.value[0], self.col + rule.value[1]
            
            while board.valid_end(row_n, col_n, self.color):
                moveset.append((row_n, col_n))
                row_n, col_n = row_n + rule.value[0], col_n + rule.value[1]
                
        return moveset
        
        
class Pawn(Piece):
    
    def __init__(self, row, col, color, identity):
        super().__init__(row, col, color, identity)
        self.moved = False
    
    #Check for pawn diagonal eat
    def moveset(self, board):
        moveset = []
        
        if self.color is Color.WHITE:
            rule = Rule.UP
            rank = 3
        else:
            rule = Rule.DOWN
            rank = 4
            
        #Normal one-step move 
        if board.valid_end(self.row + rule.value[0], self.col, self.color):
            moveset.append((self.row + rule.value[0], self.col))
            
        #Check if has not moved
        if not self.moved:
            moveset.append((self.row + 2*rule.value[0], self.col))
        
        #Check for en passant
        if self.row == rank:
            pass
        

class Rook(StrafingPiece):
    
    def __init__(self, row, col, color, identity):
        
        
        
        
        
        
        
        