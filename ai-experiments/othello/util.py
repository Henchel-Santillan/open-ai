from enum import Enum, unique
import copy


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
        

@unique
class Shade(Enum):
    
    DARK = "D"
    LIGHT = "L"
    
    @classmethod
    def values(cls):
        return [cls.DARK, cls.LIGHT]
    
    def opposite(self):
        return Shade.DARK if self is Shade.LIGHT else Shade.LIGHT
    

class Disk:
    
    def __init__(self, row, col, shade):
        self.row, self.col = row, col
        self.shade = shade
        self.flank_pairs = []
        
    def __str__(self):
        return self.shade.value
    
    def flip(self):
        self.shade = self.shade.opposite()
        

class Cell:
    
    def __init__(self, row, col):
        self.row, self.col = row, col
        self.disk = None
        
    def __str__(self):
        mark = self.disk.__str__() if self.disk is not None else " "
        return "|" + mark + "|"
    
    def put(self, disk):
        if disk is not None:
            self.disk = disk
            
    def empty(self):
        return self.disk is None
    

class Board:
    
    SIZE = 8
    HEADER = "------------------------"
    
    def __init__(self):
        self.cells = [[Cell(row, col) for col in range(Board.SIZE)]
                      for row in range(Board.SIZE)]
        
        self.cells[3][3].put(Disk(3, 3, Shade.DARK))
        self.cells[3][4].put(Disk(3, 4, Shade.LIGHT))
        self.cells[4][3].put(Disk(4, 3, Shade.LIGHT))
        self.cells[4][4].put(Disk(4, 4, Shade.DARK))
        
        self.ddisks = [self.cells[3][3].disk, self.cells[4][4].disk]
        self.ldisks = [self.cells[3][4].disk, self.cells[4][3].disk]
        
        self.spaces = Board.SIZE ** 2 - 4
        
    @staticmethod
    def in_bounds(row, col):
        return (row >= 0 and row < Board.SIZE) and (col >= 0 and col < Board.SIZE)
    
    @staticmethod
    def sameas(row1, col1, row2, col2):
        return (row1 == row2) and (col1 == col2)
    
    def draw(self):
        print(Board.HEADER)
        
        for row in range(Board.SIZE):
            for col in range(Board.SIZE):
                print(self.cells[row][col].__str__(), end="")
            
            print("\n" + Board.HEADER)
            
    def copy_board(self):
        board_copy = Board()
        board_copy.cells = copy.deepcopy(self.cells)
        return board_copy
    
    def in_dlist(self, dlist, row, col):
        return any(Board.sameas(row, col, d[0], d[1])
                   for d in dlist)
        
    def valid_moves(self, shade):
        moveset = set()
        cdisks = self.ldisks if shade is Shade.LIGHT else self.ddisks
        
        for dirn in Dirn.values():
            for cdisk in cdisks:
                opp = 0
                c_row, c_col = cdisk.row + dirn.value[0], cdisk.col + dirn.value[1]
                
                while (Board.in_bounds(c_row, c_col) and 
                       not self.cells[c_row][c_col].empty() and
                       self.cells[c_row][c_col].disk.shade is shade.opposite()):
                    opp += 1
                    c_row, c_col = c_row + dirn.value[0], c_col + dirn.value[1]
                
                #Only add if loop broken since reached empty cell
                if (Board.in_bounds(c_row, c_col) and 
                    self.cells[c_row][c_col].empty() and
                    opp > 0):
                    moveset.add((c_row, c_col))
                    cdisk.flank_pairs.append((c_row, c_col))
                    
        return moveset
                    
    def capture(self, disk):
        cdisks = self.ldisks if disk.shade is Shade.LIGHT else self.ddisks
        
        for cdisk in cdisks:
            if (disk.row, disk.col) in cdisk.flank_pairs:
                rdf, cdf = cdisk.row - disk.row, cdisk.col - disk.col
                
                if rdf != 0:
                    rdf = int(rdf / abs(rdf))
                
                if cdf != 0:
                    cdf = int(cdf / abs(cdf))
                    
                c_row, c_col = disk.row + rdf, disk.col + cdf
                
                while (c_row, c_col) != (cdisk.row, cdisk.col):
                    opp = self.cells[c_row][c_col].disk
                    
                    if disk.shade is Shade.LIGHT:
                        self.ldisks.append(opp)
                        self.ddisks.remove(opp)
                    else:
                        self.ddisks.append(opp)
                        self.ldisks.remove(opp)
                        
                    opp.flip()
                        
                    if c_row != cdisk.row:
                        c_row = c_row + rdf
                        
                    if c_col != cdisk.col:
                        c_col = c_col + cdf
                    
                cdisk.flank_pairs.remove((disk.row, disk.col))
    
    def update(self, row, col, shade):
        self.cells[row][col].put(Disk(row, col, shade))
        
        if shade is Shade.LIGHT:
            self.ldisks.append(self.cells[row][col].disk)
        else:
            self.ddisks.append(self.cells[row][col].disk)
        
        self.spaces -= 1
        self.capture(self.cells[row][col].disk)
        
    def winner(self):
        lq, dq = len(self.ldisks), len(self.ddisks)
        
        if lq == dq:
            return None
        return Shade.LIGHT if lq > dq else Shade.DARK
                    
    