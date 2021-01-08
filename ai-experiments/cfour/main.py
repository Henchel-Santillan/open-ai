from cfour.util import Board, Color
from cfour.agent import HAgent
import random, time

def main():
    print("Connect Four Console\nGet four in a row, column, or diagonal first to win.")
    time.sleep(2.0)
    
    c1 = Color.values()[random.randint(0, 1)]
    c2 = c1.opposite()
    
    p1 = HAgent(c1, "P1")
    p2 = HAgent(c2, "P2")
    cp = p1 if random.randint(0, 1) == 0 else p2
    
    board = Board()
    running = True
    
    while running:
        board.draw()
        print("TURN: " + cp.a_name + ", " + cp.color.name)
        
        m_row, m_col = cp.make_move(board)
        board.update(m_row, m_col, cp.color)
        
        if board.has_winner(m_row, m_col, cp.color):
            board.draw()
            print("\nWINNER: " + cp.a_name + ", " + cp.color.name)
            running = False
        
        if board.spaces == 0:
            board.draw()
            print("\nTIE.")
            running = False
            
        cp = p1 if cp is p2 else p2
        
main()
        
    