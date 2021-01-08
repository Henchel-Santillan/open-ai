import json
from abc import ABC, abstractmethod

from checkers.piece import Color, King


class Event(ABC):
    
    def __init__(self, start, end):
        self.start, self.end = start, end
        
    @abstractmethod
    def loggable(self):
        return self.start.__str__() + " to " + self.end.__str__()
    
    @abstractmethod
    def consume(self, board=None):
        pass
    

class Move(Event):
    
    def __init__(self, start, end):
        super().__init__(start, end)
        
    def loggable(self):
        return "Move: " + super().loggable()
    
    def consume(self, board=None):
        self.end.put(self.start.piece)
        self.start.clear()
        
        
class Eat(Move):
    
    def __init__(self, start, end, middle):
        super().__init__(start, end)
        self.middle = middle
        
    def loggable(self):
        return "Eat+" + super().loggable()
    
    def consume(self, board):
        super().consume()
        
        if self.middle.piece.color is Color.BLACK:
            board.bpieces.remove(self.middle.piece)
        else:
            board.rpieces.remove(self.middle.piece)
        
        self.middle.clear()
        

class Crown(Move):
    
    def __init__(self, start, end):
        super().__init__(start, end)
        
    def loggable(self):
        return "Crown+" + super().loggable()
    
    def consume(self, board):
        super().consume()
        king = King(self.end.row, self.end.col, self.end.piece.color)
        self.end.put(king)
        
        if self.end.piece.color is Color.BLACK:
            board.bpieces.remove(self.end.piece)
            board.bpieces.append(king)
        else:
            board.rpieces.remove(self.end.piece)
            board.rpieces.append(king)
        
        
class Logger:
    
    def __init__(self):
        self.log = []
        
    def log(self, event):
        self.log.append(event)
        
    def nread(self, path, label=None):
        try:
            with open(path, 'r') as file:
                for line in file:
                    print(line)
                    
        except IOError as error:
            print(error)
            if label is not None:   
                label.setText("File error occurred. Cannot read from file.")
                
    def gnread(self, path, label=None):
        try:
            with open(path, 'r') as file:
                for line in file:
                    yield line
                    
        except IOError as error:
            print(error)
            if label is not None:
                label.setText("File error occurred. Cannot read from file.")
                
    def rnread(self, path, label=None):
        try:
            with open(path, 'r') as file:
                return file.read().split("\n")
            
        except IOError as error:
            print(error)
            if label is not None:
                label.setText("File error occurred. Cannot read from file.")
                
    def jsonread(self, path, label=None):
        pass
                
    def nwrite(self, path, label=None):
        try:
            with open(path, 'w') as file:
                for event in self.log:
                    file.write(event.loggable() + "\n")
                    
        except IOError as error:
            print(error)
            if label is not None:
                label.setText("File error occurred. Cannot write to file.")
                
    def gnwrite(self, path, label=None):
        pass
    
    def jsonwrite(self, path, label=None):
        pass
        
        