import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import (QApplication, QWidget, QFileDialog, QVBoxLayout, QHBoxLayout,
                             QGridLayout, QLineEdit, QPushButton, QLabel)
from PyQt5.QtGui import QIntValidator, QPainter

from sudoku.solver import solve

class SudokuApp(QWidget):
    
    BOARD_DIM = 9
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Sudoku Puzzle Solver")
        self.layout = QVBoxLayout()
        
        self.grid = QGridLayout()
        
        for row in range(SudokuApp.BOARD_DIM):
            for col in range(SudokuApp.BOARD_DIM):
                qle = QLineEdit()
                qle.setMaxLength(1)
                qle.setValidator(QIntValidator(1, 9, self))
                
                qle.setMaximumWidth(
                    qle.fontMetrics().boundingRect("000").width())
                qle.setAlignment(QtCore.Qt.AlignCenter)
                        
                self.grid.addWidget(qle, *(row, col))
        
        self.label = QLabel()
        
        upload = QPushButton("Upload")
        upload.clicked.connect(lambda: self.c_upload())
        
        clear = QPushButton("Clear")
        clear.clicked.connect(lambda: self.c_clear())
        
        solve = QPushButton("Solve")
        solve.clicked.connect(lambda: self.c_solve())
        
        self.panel = QHBoxLayout()
        self.panel.addWidget(upload)
        self.panel.addWidget(clear)
        self.panel.addWidget(solve)
        
        self.layout.addLayout(self.grid)
        self.layout.addWidget(self.label)
        self.layout.addLayout(self.panel)
        self.setLayout(self.layout)
        
        self.setFixedSize(400, 400)
    
    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        qp.drawLine(25, 102, 370, 102)
        qp.drawLine(25, 195, 370, 195)
        qp.drawLine(136, 15, 136, 285)
        qp.drawLine(255, 15, 255, 285)
        qp.end()
    
    #Add push button icon beside c_upload that brings up info dialog specifying file format
    def c_upload(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open File", "",
                                                  "Text Files (*.txt)", options = QFileDialog.Options())
        if fileName:
            self.label.setText("Uploaded: " + fileName)
            
            with open(fileName, 'r') as file:
                index = 0
                lines = [line.strip() for line in file]
                
                for line in lines:
                    for token in line:
                            self.grid.itemAt(index).widget().setText(token)
                            index += 1
    
    #advanced options: e.g. clear all, clear all of 1 - 9, etc. clear column, clear row
    #mouse_event may also trigger clear
    def c_clear(self):
        index = 0
        
        while index < self.grid.count():
            self.grid.itemAt(index).widget().setText("")
            index += 1
        
    def c_solve(self):
        lboard = [[0] * SudokuApp.BOARD_DIM for _ in range(SudokuApp.BOARD_DIM)]
        
        try:
            for row in range(SudokuApp.BOARD_DIM):
                for col in range(SudokuApp.BOARD_DIM):
                    index = SudokuApp.BOARD_DIM * row + col
                    
                    if self.grid.itemAt(index).widget().text().strip() != "":
                        val = int(self.grid.itemAt(index).widget().text())
                    
                    if val != 0:
                        lboard[row][col] = val
                    
            solved = solve(lboard)
            
            if solved:
                self.label.setText("Solution found.")
                
                for row in range(SudokuApp.BOARD_DIM):
                    for col in range(SudokuApp.BOARD_DIM):
                        index = SudokuApp.BOARD_DIM * row + col
                
                        self.grid.itemAt(index).widget().setText(str(
                            lboard[row][col]))
                
            else:
                self.label.setText("No solution found.")
                
                        
        except ValueError:
            self.label.setText("Bad input.")
    
        
if __name__ == "__main__":
    application = QApplication([])
    
    window = SudokuApp()
    window.show()
    
    sys.exit(application.exec_())
    