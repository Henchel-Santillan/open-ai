 import random

from checkers.board import Board, Color
from checkers.agent import HAgent
from checkers.event import Eat

def main():
    print("Checkers Console\nCapture all pieces or force your opponent to have no plays to win.")
    
    c1 = Color.values()[random.randint(0, 1)]
    c2 = c1.opposite()
    
    p1 = HAgent(c1, "P1")
    p2 = HAgent(c2, "P2")
    
    cp = p1 if random.randint(0, 1) == 0 else p2
    
    board = Board()
    running = True

    #NEW DESIGN: DO THE TRUTHY CHECK FOR IS_NEXT IN THE GAME LOOP, LET MAKE_MOVE BE
    #DECISION FOR MOVE, EAT, CROWN, ETC.
    #TRANSFER THE ROW1, COL1 VALUES HERE
    while running:
        board.draw()
        print("TURN: " + cp.a_name + ", " +  cp.color.name)
        
        mnext = board.mnext(cp.color)
        
        if not mnext:
            if cp is p1:
                print("WINNER: " + p2.a_name + ", " + p2.color.name)
            else:
                print("WINNER: " + p1.a_name + ", " + p1.color.name)
            
            running = False
            break
        
        print("\nELIGIBLE PIECES: ")
        for piece in mnext:
            print("(" + str(piece.row + 1) + ", " + str(piece.col + 1) + ")", end=" ")
        
        print()
        mrow1, mcol1 = int(input("\nROW: ")), int(input("COLUMN: "))
        
        while not any((mrow1, mcol1) == (p.row, p.col) for p in mnext):
            print("\nENTER (ROW,COL) FOR ELIGIBLE PIECES ONLY.")
            mrow1, mcol1 = int(input("\nROW: ")), int(input("COLUMN: "))
        
        #premature False: improve bool ordering
        mrow2, mcol2 = cp.make_move(board, mrow1, mcol1, False)
        
        update = board.update(mrow1, mcol1, mrow2, mcol2, cp.color)
        
        while isinstance(update, Eat):
            mrow1, mcol1 = mrow2, mcol2
            mrow2, mcol2 = cp.make_move(board, mrow1, mcol1, True)
            update = board.update(mrow1, mcol1, mrow2, mcol2, cp.color)
                
        if board.winner():
            pass
        
        cp = p1 if cp is p2 else p1
    
main()