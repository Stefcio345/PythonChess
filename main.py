from Classes.Board import ChessBoard
from Classes.ChessEngine import ChessEngine
from Classes.Cursor import Cursor
from Classes.BoardState import BoardState

# Prepare board
board = ChessBoard()
state = BoardState(board.getBoardState())
board.setBoardState(state)
chessEngine = ChessEngine(state, "White")
mate = False
boardCursor = Cursor(7, 7)
board.printBoard()

#TODO Menu
#TODO save/load

# GameLoop
while True:
    if boardCursor.move():
        cursorPos = boardCursor.getPos()

        # If second tile was selected
        if boardCursor.prevSelectedPos is not None:
            # Try to make a move
            if chessEngine.makeMove(boardCursor.prevSelectedPos, boardCursor.selectedPos, state):
                mate = chessEngine.checkIfMate(state)
                boardCursor.unSelect()

        # Update board after move
        chessEngine.updateBoard(cursorPos, boardCursor.selectedPos, state)

        board.setBoardState(state)
        board.printBoard()

        if mate:
            print(f"{ChessEngine.currentColor} WINS!!!!")
            break
