import copy 

from checkers.piece import Draught, Color
from checkers.event import Move, Eat, Crown, Logger


class Cell:
    
    def __init__(self, row, col):
        self.row, self.col = row, col
        self.piece = None
        
    def __str__(self):
        return "(" + str(self.row + 1) + ", " + str(self.col + 1) + ")"
    
    def draw(self):
        mark = self.piece.__str__() if not self.empty() else "  "
        print("|" + mark + "|", end="")
    
    def put(self, piece):
        if piece is not None:
            self.piece = piece
            self.piece.update_pos(self.row, self.col)
            
    def clear(self):
        self.piece = None
        
    def empty(self):
        return self.piece is None
    
    
class Board:
    
    SIZE = 8
    HEADER = "------------------------"
    
    def __init__(self):
        self.cells = []
        
        self.bpieces = []
        self.rpieces = []
        
        for row in range(Board.SIZE):
            c_row = []
            
            for col in range(Board.SIZE):
                cell = Cell(row, col)
                
                if (row not in range(3, 4) and 
                    ((row % 2 == 0 and col % 2 != 0) or
                     (row % 2 != 0 and col % 2 == 0))):
                    
                    if row < 3:
                        cell.put(Draught(row, col, Color.BLACK))
                        self.bpieces.append(cell.piece)
                    else:
                        cell.put(Draught(row, col, Color.RED))
                        self.wpieces.append(cell.piece)
                        
                c_row.append(cell)
            
            self.cells.append(c_row)
            
            self.logger = Logger()
            
    @staticmethod 
    def in_bounds(row, col):
        return (row >= 0 and row < Board.SIZE) and (col >= 0 and col < Board.SIZE)
    
    def draw(self):
        print(Board.HEADER)
        
        for row in range(Board.SIZE):
            for col in range(Board.SIZE):
                self.cells[row][col].draw()
            
            print("\n" + Board.HEADER)
            
    def copy_board(self):
        board_copy = Board()
        board_copy.cells = copy.deepcopy(self.cells)
        return board_copy

    def mnext(self, color):
        pieces = self.bpieces if color is Color.RED else self.rpieces
        mnext = []
        
        for piece in pieces:
            moveset = piece.valid_moves(self)
            
            if moveset[0] or moveset[1]:
                mnext.append(piece)
                
        return mnext

    def update(self, row1, col1, row2, col2, color):
        event = None
        
        scell = self.cells[row1][col1]
        ecell = self.cells[row2][col2]
        
        if abs(row2 - row1) == 1:
            
            if (isinstance(scell.piece, Draught) and
                ((color is Color.RED and row2 == 0) or
                 color is Color.BLACK and row2 == 7)):
                event = Crown(scell, ecell)
            
            else:
                event = Move(scell, ecell)
                
        else:
            rf, cf = (row2 - row1) / 2, (col2 - col1) / 2
            event = Eat(scell, ecell, self.cells[row1 + rf][col1 + cf])

        event.consume()
        self.logger.log(event) 
        
        return event
    
    def winner(self):
        return Color.BLACK if not self.rpieces else Color.RED
                