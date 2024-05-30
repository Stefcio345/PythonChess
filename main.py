from Classes.Board import ChessBoard
from Classes.ChessEngine import ChessEngine
from Classes.Cursor import Cursor
from Classes.BoardState import BoardState



# Prepare board
board = ChessBoard()
state = BoardState(board.getBoardState())
board.setBoardState(state)
chessEngine = ChessEngine()
chessEngine.updateStates(state)
possibleMoves = []
mate = False
boardCursor = Cursor(7, 7)
board.printBoard()
currentColor = "White"

#TODO Menu
#TODO save/load

# GameLoop
while True:
    prevCursorPos = boardCursor.getPos()
    prevSelectedPos = boardCursor.selectedPos
    if boardCursor.move():
        cursorPos = boardCursor.getPos()

        selectedPos = boardCursor.selectedPos

        # If piece was selected
        if chessEngine.updateBoard(cursorPos, selectedPos, state) and prevSelectedPos is not None:
            # Try to make a move
            if chessEngine.makeMove(prevSelectedPos, selectedPos, state):
                mate = chessEngine.checkIfMate(state)
                boardCursor.selectedPos = None

        board.setBoardState(state)
        board.printBoard()

        if mate:
            print(f"{ChessEngine.currentColor} WINS!!!!")
            break
