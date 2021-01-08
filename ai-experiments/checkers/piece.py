from enum import Enum, unique
from abc import ABC, abstractmethod

from checkers.board import Board


@unique
class Color(Enum):
    BLACK = "B"
    RED = "R"
    
    @classmethod
    def values(cls):
        return [cls.BLACK, cls.RED]
    
    def opposite(self):
        return Color.BLACK if self is Color.RED else Color.RED
    
    
@unique
class Dirn(Enum):
    UPL = (-1, -1)
    DOWNR = (1, 1)
    UPR = (-1, 1)
    DOWNL = (1, -1)
    
    @classmethod 
    def values(cls):
        return [cls.UPL, cls.DOWNR, cls.UPR, cls.DOWNL]
    
    def opposite(self):
        for dirn in Dirn.values():
            if (-self.value[0], -self.value[1]) == (dirn.value[0], dirn.value[1]):
                return dirn
            
        return None
    

class Piece(ABC):
    
    def __init__(self, row, col, color):
        self.row, self.col = row, col
        self.color = color
        
    def __str__(self):
        return self.color.value
    
    @classmethod
    def sameas(cls, row1, col1, row2, col2):
        return (row1, col1) == (row2, col2)
    
    def in_moveset(self, moveset, row, col):
        return any(Piece.sameas(row, col, move[0], move[1])
                   for move in moveset)
        
    def get_neighbors(self, origin):
        neighbors = []
        
        for dirn in self.base_dirns():
            row, col = origin.row + dirn.value[0], origin.col + dirn.value[1]
            
            if Board.in_bounds(row, col):
                neighbors.append((row, col))
                
        return neighbors
    
    def valid_moves(self, board):
        eats = []
        moves = self.get_neighbors(board.cells[self.row][self.col])
        
        for move in moves:
            c_cell = board.cells[move[0]][move[1]]
            
            if (not c_cell.empty() and
                c_cell.piece.color is self.color.opposite()):
                
                eats.extend(self.get_neighbors(
                    board.cells[c_cell.row][c_cell.col]))
                moves.remove(move)
                
        return moves, list(filter(lambda x: x.col != self.col, eats))
        
    def update_pos(self, row, col):
        self.row, self.col = row, col
        
    @abstractmethod 
    def base_dirns(self):
        pass
    

class Draught(Piece):
    
    def __init__(self, row, col, color):
        super().__init__(row, col, color)
    
    def __str__(self):
        return super().__str__() + "D"
    
    def base_dirns(self):
        return Dirn.values()[0::2] if self.color is Color.RED else Dirn.values[1::2]


class King(Piece):
    
    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        
    def __str__(self):
        return super().__str__() + "K"
    
    def base_dirns(self):
        return Dirn.values()
                