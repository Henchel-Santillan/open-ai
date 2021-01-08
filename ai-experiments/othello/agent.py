from abc import ABC, abstractmethod

class Agent(ABC):
    
    def __init__(self, shade, a_name):
        self.shade = shade
        self.a_name = a_name
        
    @abstractmethod
    def make_move(self, board):
        pass
    

class HAgent(Agent):
    
    def __init__(self, shade, a_name):
        super().__init__(shade, a_name)
        
    def make_move(self, board):
        moveset = sorted(board.valid_moves(self.shade))
        
        if not moveset:
            return -1, -1
        
        print("MOVES\n")
        
        for move in moveset:
            print("(" + str(move[0]) + ", " + str(move[1]) + ")", end=" ")
        
        print()
        row, col = int(input("\nROW: ")), int(input("COLUMN: "))
        
        while not board.in_dlist(moveset, row, col):
            print("INPUT (ROW, COL) IN MOVES ONLY.")
            row, col = int(input("\nROW: ")), int(input("COLUMN: "))
            
        return row, col 
        
        
class RandAgent(Agent):
    
    def __init__(self, shade, name):
        super().__init__(shade, name)
        
    def make_move(self, board):
        moveset = board.valid_moves(self.shade)
        
        if not moveset:
            return -1, -1
        
        for move in moveset:
            break
        
        return move[0], move[1]
    
    
        