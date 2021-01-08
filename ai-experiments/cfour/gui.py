import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class CFourApplet(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Connect Four")
        self.layout = QVBoxLayout
        self.setLayout(self.layout)
        
        #Top Screen Title
        title = QLabel("Connect Four")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Times", 24))
        self.layout.addWidget(title)
        
        #Control Panel for player(s)
        self.panel = QHBoxLayout()
        
        self.reset = QPushButton("Reset")
        self.reset.setEnabled(False)
        self.reset.clicked.connect(lambda: self.reset())
        
        
    def reset(self):
        pass

if __name__ == "__main__":
    application = QApplication([])
    window = CFourApplet()
    window.show()
    sys.exit(application.exec_())