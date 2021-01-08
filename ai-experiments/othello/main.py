from othello.agent import HAgent
from othello.util import Board, Shade

import random, time

def main():
    print("Othello Console\nCapture the most squares to win.")
    time.sleep(2.5)
    
    s1 = Shade.values()[random.randint(0, 1)]
    s2 = s1.opposite()
    
    p1 = HAgent(s1, "P1")
    p2 = HAgent(s2, "P2")
    cp = p1 if s1 is Shade.DARK else p2
    
    board = Board()
    running = True
    
    p1_go, p2_go = True, True
    
    while running:
        board.draw()
        print("TURN: " + cp.a_name + ", " + cp.shade.name)
        m_row, m_col = cp.make_move(board)
        
        if m_row == -1 and m_col == -1:
            print(cp.name + " CANNOT PLAY. TURN SKIPPED.")
            
            if cp is p1:
                p1_go = False
            else:
                p2_go = False
        else:
            board.update(m_row, m_col, cp.shade)
        
        if board.spaces == 0 or not(p1_go or p2_go):
            winner = board.winner()
            
            if winner is not None:
                print("\nWINNER: " + winner.name)
            else:
                print("\nTIE.")
                
            running = False
        
        cp = p1 if cp is p2 else p2
    
main()

