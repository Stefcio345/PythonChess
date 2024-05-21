from Classes.Board import ChessBoard
from Classes.ChessEngine import ChessEngine

testState = [[('Reset', 'Empty'), ('Reset', 'Empty'), ('Black', 'Bishop'), ('Black', 'Queen'), ('Reset', 'Empty'), ('Black', 'Bishop'), ('Black', 'Knight'), ('Black', 'Rook')],
[('Black', 'Pawn'), ('Black', 'Pawn'), ('Black', 'Pawn'), ('Black', 'Pawn'), ('Reset', 'Empty'), ('Black', 'Pawn'), ('Black', 'Pawn'), ('Black', 'Pawn')],
[('Reset', 'Empty', 'Whitebg'), ('Reset', 'Empty'), ('Black', 'Knight'), ('Reset', 'Empty'), ('Reset', 'Empty'), ('Reset', 'Empty'), ('Reset', 'Empty'), ('Reset', 'Empty')],
[('Reset', 'Empty'), ('Reset', 'Empty'), ('Reset', 'Empty'), ('Reset', 'Empty'), ('Black', 'Pawn'), ('Reset', 'Empty'), ('Reset', 'Empty'), ('Reset', 'Empty')],
[('Reset', 'Empty'), ('Reset', 'Empty'), ('White', 'Queen'), ('White', 'Pawn'), ('Black', 'King'), ('White', 'Bishop'), ('Reset', 'Empty'), ('Reset', 'Empty')],
[('Reset', 'Empty'), ('Black', 'Rook'), ('Reset', 'Empty'), ('Reset', 'Empty'), ('Reset', 'Empty'), ('Reset', 'Empty'), ('Reset', 'Empty'), ('Reset', 'Empty')],
[('White', 'Pawn'), ('White', 'Pawn'), ('White', 'Pawn'), ('Reset', 'Empty'), ('White', 'Pawn'), ('White', 'Pawn'), ('White', 'Pawn'), ('White', 'Pawn')],
[('White', 'Rook'), ('White', 'Knight'), ('Reset', 'Empty'), ('Reset', 'Empty'), ('White', 'King'), ('White', 'Bishop'), ('White', 'Knight'), ('White', 'Rook')]]

board = ChessBoard()
board.printBoard()

chessEngine = ChessEngine()
chessEngine.highlightPossibleMoves(chessEngine.getMoves(7, 6, testState), testState)

board.setBoardState(testState)
board.printBoardState()
board.printBoard()

