import sys
import random

from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
                             QPushButton, QLabel, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from tictactoe.solver import full, winner, ab_best_move

class TTTApp(QWidget): 
    
    DIM = 3
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("TicTacToe AI")
        self.layout = QVBoxLayout()
        title = QLabel("TicTacToe")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Times", 20))
        self.layout.addWidget(title)
        
        self.grid = QGridLayout()
        self.layout.addLayout(self.grid)
        
        self.bgrid = [[""] * TTTApp.DIM for _ in range(TTTApp.DIM)]
        
        for row in range(TTTApp.DIM):
            for col in range(TTTApp.DIM):
                cell = QPushButton()
                cell.setGeometry(90 * row + 20, 90 * col + 20, 80, 80)
                cell.setFont(QFont("Times", 17))
                
                cell.clicked.connect(lambda: self.update())
                
                self.grid.addWidget(cell, *(row, col))
                
        self.label = QLabel()
        self.label.setGeometry(20, 300, 260, 60)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("QLabel"
                                 "{"
                                 "border : 3px solid black"
                                 "background : white"
                                 "}")
        self.label.setFont(QFont("Times", 15))
        self.layout.addWidget(self.label)
        
        self.log = QLabel()
                
        self.solve = QPushButton("Solve")
        self.solve.clicked.connect(lambda: self.solve())
        
        self.reset = QPushButton("Reset")
        self.reset.clicked.connect(lambda: self.reset())
        
        self.movelog = QPushButton("Move Log")
        self.movelog.setEnabled(False)
        self.movelog.clicked.connect(lambda: self.get_log())
        
        self.panel = QHBoxLayout()
        self.panel.addWidget(self.solve)
        self.panel.addWidget(self.reset)
        self.panel.addWidget(self.movelog)
        
        self.layout.addLayout(self.panel)
        self.setLayout(self.layout)
        
        self.cp = 'X' if random.randint(0, 1) == 0 else 'O'
        self.fp = self.cp
    
    def update(self):
        button = self.sender()
        button.setText(self.cp)
        button.setEnabled(False)
        
        index = self.grid.indexOf(button)
        row, col = int(abs(index - TTTApp.DIM) / 3), index % TTTApp.DIM
        self.bgrid[row][col] = button.text()
        
        self.log.setText(self.log.text()  
                        + "(" 
                        +str(row) 
                        + ", "
                        + str(col)
                        + ") ")
        
        pwinner = winner(self.bgrid, self.fp)
        
        if pwinner is not None:
            self.lock()
            self.label.setText("Winner is " + self.cp)
            self.movelog.setEnabled(True)
        
        self.cp = 'X' if self.cp == 'O' else 'O'
        
    def lock(self):
        index = 0
        
        while index < self.grid.count():
            button = self.grid.itemAt(index).widget()
            
            if button.isEnabled():
                button.setEnabled(False)
                
            index += 1
        
    def reset(self):
        index = 0
        
        while index < self.grid.count():
            button = self.grid.itemAt(index).widget()
            button.setText("")
            button.setEnabled(True)
            index += 1
        
        self.bgrid.clear()
        self.label.setText("")
        self.movelog.setEnabled(False)
        self.cp = 'X' if random.randint(0, 1) == 0 else 'O'
        self.fp = self.cp
    
    def solve(self):
        while not full(self.bgrid):
            row, col = ab_best_move(self.bgrid, self.fp)
            self.bgrid[row][col].setText(self.cp)
            self.grid.itemAt(TTTApp.DIM * row + col).widget().click()
    
    def get_log(self):
        dialog = QMessageBox()
        dialog.setText("Moves for the game\n" + self.log)
        dialog.exec_()
    
    
if __name__ == "__main__":
    application = QApplication([])
    window = TTTApp()
    window.show()
    sys.exit(application.exec_())
        