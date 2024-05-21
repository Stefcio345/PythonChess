from Classes.Board import ChessBoard

testState = [[('Black', 'Rook'), ('Reset', 'Empty'), ('Black', 'Bishop'), ('Black', 'Queen'), ('Black', 'King'), ('Black', 'Bishop'), ('Black', 'Knight'), ('Black', 'Rook')],
[('Black', 'Pawn'), ('Black', 'Pawn'), ('Black', 'Pawn'), ('Black', 'Pawn'), ('Reset', 'Empty'), ('Black', 'Pawn'), ('Black', 'Pawn'), ('Black', 'Pawn')],
[('Reset', 'Empty'), ('Reset', 'Empty'), ('Black', 'Knight'), ('Reset', 'Empty'), ('Reset', 'Empty'), ('Reset', 'Empty'), ('Reset', 'Empty'), ('Reset', 'Empty')],
[('Reset', 'Empty'), ('Reset', 'Empty'), ('Reset', 'Empty'), ('Reset', 'Empty'), ('Black', 'Pawn'), ('Reset', 'Empty'), ('Reset', 'Empty'), ('Reset', 'Empty')],
[('Reset', 'Empty'), ('Reset', 'Empty'), ('Reset', 'Empty'), ('White', 'Pawn'), ('Reset', 'Empty'), ('White', 'Bishop'), ('Reset', 'Empty'), ('Reset', 'Empty')],
[('Reset', 'Empty'), ('Reset', 'Empty'), ('Reset', 'Empty'), ('Reset', 'Empty'), ('Reset', 'Empty'), ('Reset', 'Empty'), ('Reset', 'Empty'), ('Reset', 'Empty')],
[('White', 'Pawn'), ('White', 'Pawn'), ('White', 'Pawn'), ('Reset', 'Empty'), ('White', 'Pawn'), ('White', 'Pawn'), ('White', 'Pawn'), ('White', 'Pawn')],
[('White', 'Rook'), ('White', 'Knight'), ('Reset', 'Empty'), ('White', 'Queen'), ('White', 'King'), ('White', 'Bishop'), ('White', 'Knight'), ('White', 'Rook')]]

board = ChessBoard()
board.printBoard()

board.setBoardState(testState)
board.printBoard()
