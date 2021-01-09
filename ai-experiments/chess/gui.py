import sys
from PyQt5.QtWidgets import QApplication, QWidget


class UIChess(QWidget):
    
    def __init__(self):
        super().__init__()
        

if __name__ == "__main__":
    application = QApplication([])
    window = UIChess()
    window.show()
    sys.exit(application.exec_())