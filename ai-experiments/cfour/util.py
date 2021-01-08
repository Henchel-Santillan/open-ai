from enum import Enum, unique
import copy
import numpy as np

@unique
class Dirn(Enum):
    
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)
    UPL = (-1, -1)
    DOWNR = (1, 1)
    UPR = (-1, 1)
    DOWNL = (1, -1)
    
    @classmethod
    def values(cls):
        return [cls.UP, cls.DOWN, cls.LEFT, cls.RIGHT,
                cls.UPL, cls.DOWNR, cls.UPR, cls.DOWNL]
        
    def opposite(self):
        for dirn in Dirn.values():
            if (-self.value[0], -self.value[1]) == (dirn.value[0], dirn.value[1]):
                return dirn
        
        return None
        
        
@unique
class Color(Enum):
    
    BLACK = "B"
    RED = "R"
    
    @classmethod
    def values(cls):
        return [cls.BLACK, cls.RED]
    
    def opposite(self):
        return Color.BLACK if self is Color.RED else Color.RED
    
    
class Chip:
    
    def __init__(self, row, col, color):
        self.row, self.col = row, col
        self.color = color
        
    def __str__(self):
        return self.color.value


class Cell:
    
    def __init__(self, row, col):
        self.row, self.col = row, col
        self.chip = None
        
    def __str__(self):
        mark = self.chip.__str__() if self.chip is not None else " "
        return "|" + mark + "|"
    
    def put(self, chip):
        if chip is not None:
            self.chip = chip
            
    def empty(self):
        return self.chip is None
    
    
class Board:
    
    ROW = 6
    COL = 7
    WIN_VAL = 4
    
    HEADER = "---------------------"
    
    def __init__(self):
        self.cells = [[Cell(row, col) for col in range(Board.COL)]
                      for row in range(Board.ROW)]
        
        self.spaces = Board.ROW * Board.COL
        
    @staticmethod
    def in_bounds(row, col):
        return (row >= 0 and row < Board.ROW) and (col >= 0 and col < Board.COL)
    
    @staticmethod
    def sameas(row1, col1, row2, col2):
        return (row1 == row2) and (col1 == col2)
    
    def copy_board(self):
        board_copy = Board()
        board_copy.cells = copy.deepcopy(self.cells)
        return board_copy
    
    #Incorrect representation of bitboard
    def to_bitboard(self, color):
        bitboard = np.zeros((Board.ROW, Board.COL))
        
        for row in range(Board.ROW):
            for col in range(Board.COL):
                if (not self.cells[row][col].empty() and 
                    self.cells[row][col].chip.color is color):
                    bitboard[row][col] = 1
                
        return bitboard    
    
    def draw(self):
        print(Board.HEADER)
        
        for row in range(Board.ROW):
            for col in range(Board.COL):
                print(self.cells[row][col].__str__(), end="")
            
            print("\n" + Board.HEADER)
            
    def in_moveset(self, moveset, row, col):
        return any(Board.sameas(row, col, move[0], move[1]) 
                   for move in moveset)
        
    def valid_moves(self):
        moveset = []
        row = Board.ROW - 1
        
        for col in range(Board.COL):
            while row >= 0 and not self.cells[row][col].empty():
                row -= 1
            
            if row != -1:
                moveset.append((row, col))
                
            row = Board.ROW - 1
            
        return moveset
    
    def update(self, row, col, color):
        self.cells[row][col].put(Chip(row, col, color))
        self.spaces -= 1
        
    def valid_next(self, row, col, color):
        return (Board.in_bounds(row, col) and 
                not self.cells[row][col].empty() and
                self.cells[row][col].chip.color is color)    
    
    def has_winner(self, row, col, color):
        bdirns = Dirn.values()[0::2]
        
        for bdirn in bdirns:
            count = 1
            odirn = bdirn.opposite()
            
            brow, bcol = row + bdirn.value[0], col + bdirn.value[1]
            orow, ocol = row + odirn.value[0], col + odirn.value[1]
            
            bvalid = self.valid_next(brow, bcol, color)
            ovalid = self.valid_next(orow, ocol, color)
            
            while bvalid or ovalid:
                if bvalid:
                    count += 1
                    brow, bcol = brow + bdirn.value[0], bcol + bdirn.value[1]
                    
                    bvalid = self.valid_next(brow, bcol, color)
                    
                if ovalid:
                    count += 1
                    orow, ocol = orow + odirn.value[0], ocol + odirn.value[1]
                    
                    ovalid = self.valid_next(orow, ocol, color)
            
            if count == Board.WIN_VAL:
                return True
        
        return False
    