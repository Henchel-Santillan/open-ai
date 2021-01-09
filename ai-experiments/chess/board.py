import chess.formatter
from chess.piece import Color


class Cell:
    
    def __init__(self, row, col):
        self.row, self.col = row, col
        self.piece = None
        
    def __str__(self):
        return "(" + str(self.row+1) + ", " + str(self.col+1) + ")"
    
    def uci(self):
        pass
    
    def draw(self):
        pass
    
    def put(self, piece):
        if piece is not None:
            self.piece = piece
            self.piece.update(self.row, self.col)
            
    def clear(self):
        self.piece = None
    
    def empty(self):
        return self.piece is None
    
    
class Board:
    
    SIZE = 8
    
    def __init__(self):
        self.cells = [[Cell(row, col) for col in range(Board.SIZE)]
                      for row in range(Board.SIZE)]
        
    @staticmethod
    def in_bounds(row, col):
        return (row >= 0 and row < Board.SIZE) and (col >= 0 and col < Board.SIZE)
    
    def valid_start(self, row, col, color):
        return (Board.in_bounds(row, col) and 
                not self.cells[row][col].empty() and 
                self.cells[row][col].piece.color is color)
        
    def valid_end(self, row, col, color):
        return (Board.in_bounds(row, col) and 
                (self.cells[row][col].empty() or 
                 (not self.cells[row][col].empty() and 
                  self.cells[row][col].piece.color is not color)))
        
    
        
        
        
        
        