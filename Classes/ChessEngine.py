class ChessEngine:

    def getMoves(self, row, col, boardState):
        piece = boardState[row][col][1]
        color = boardState[row][col][0]

        if self.isCheck(boardState, color):
            match piece:
                case "King":
                    return self.getKingMoves(row, col, boardState)
        match piece:
            case "Pawn":
                return self.getPawnMoves(row, col, boardState)
            case "Rook":
                return self.getRookMoves(row, col, boardState)
            case "Bishop":
                return self.getBishopMoves(row, col, boardState)
            case "Knight":
                return self.getKnightMoves(row, col, boardState)
            case "Queen":
                return self.getQueenMoves(row, col, boardState)
            case "King":
                return self.getKingMoves(row, col, boardState)
            case _:
                return []

    def getAttacks(self, row, col, boardState):
        piece = boardState[row][col][1]
        match piece:
            case "Pawn":
                return self.getPawnAttacks(row, col, boardState)
            case "Rook":
                return self.getRookMoves(row, col, boardState)
            case "Bishop":
                return self.getBishopMoves(row, col, boardState)
            case "Knight":
                return self.getKnightMoves(row, col, boardState)
            case "Queen":
                return self.getQueenMoves(row, col, boardState)
            case _:
                return []

    def getAllMoves(self, boardState, color=""):
        allMoves = set()
        for indexY, row in enumerate(boardState):
            for indexX, tile in enumerate(row):
                if tile[0] == color or color == "":
                    possibleMoves = self.getMoves(indexY, indexX, boardState)
                    if len(possibleMoves) > 0:
                        allMoves.update(possibleMoves)

        return allMoves

    def getAllAttacks(self, boardState, color=""):
        allMoves = set()
        for indexY, row in enumerate(boardState):
            for indexX, tile in enumerate(row):
                if tile[0] == color or color == "":
                    possibleMoves = self.getAttacks(indexY, indexX, boardState)
                    if len(possibleMoves) > 0:
                        allMoves.update(possibleMoves)

        return allMoves

    def getPawnMoves(self, row, col, boardState):

        possibleMoves = []
        allyColor = boardState[row][col][0]

        #Check movement
        if allyColor == "White":
            endRow = row - 1
            if boardState[endRow][col][1] == "Empty" and 0 <= endRow <= 7:
                possibleMoves.append((endRow, col))
                endRow = endRow - 1
                if boardState[endRow][col][1] == "Empty" and row == 6:
                    possibleMoves.append((endRow, col))
        if allyColor == "Black":
            endRow = row + 1
            if boardState[endRow][col][1] == "Empty" and 0 <= endRow <= 7:
                possibleMoves.append((endRow, col))
                endRow = endRow + 1
                if boardState[endRow][col][1] == "Empty" and row == 1:
                    possibleMoves.append((endRow, col))

        #Check Attacks
        possibleBlackAttacks = ((1, -1), (1, 1))
        possibleWhiteAttacks = ((-1, -1), (-1, 1))

        if allyColor == "White":
            for move in possibleWhiteAttacks:
                endRow = row + move[0]
                endCol = col + move[1]
                if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                    if boardState[endRow][endCol][0] == "Black":
                        possibleMoves.append((endRow, endCol))

        if allyColor == "Black":
            for move in possibleBlackAttacks:
                endRow = row + move[0]
                endCol = col + move[1]
                if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                    if boardState[endRow][endCol][0] == "White":
                        possibleMoves.append((endRow, endCol))

        return possibleMoves

    def getPawnAttacks(self, row, col, boardState):

        possibleMoves = []
        allyColor = boardState[row][col][0]

        #Check Attacks
        possibleBlackAttacks = ((1, -1), (1, 1))
        possibleWhiteAttacks = ((-1, -1), (-1, 1))

        if allyColor == "White":
            for move in possibleWhiteAttacks:
                endRow = row + move[0]
                endCol = col + move[1]
                if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                    if boardState[endRow][endCol][0] == "Black":
                        possibleMoves.append((endRow, endCol))

        if allyColor == "Black":
            for move in possibleBlackAttacks:
                endRow = row + move[0]
                endCol = col + move[1]
                if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                    if boardState[endRow][endCol][0] == "White":
                        possibleMoves.append((endRow, endCol))

        return possibleMoves


    def getKnightMoves(self, row, col, boardState):

        knightMoves = ((-2, -1), (-2, 1), (-1, 2), (1, 2), (2, -1), (2, 1), (-1, -2), (1, -2))
        possibleMoves = []
        allyColor = boardState[row][col][0]

        for move in knightMoves:
            endRow = row + move[0]
            endCol = col + move[1]
            if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                endPiece = boardState[endRow][endCol]
                if endPiece[0] != allyColor:  # so its either enemy piece or empty square
                    possibleMoves.append((endRow, endCol))

        return possibleMoves

    def getRookMoves(self, row, col, boardState):
        RookMoves = ((-1, 0), (1, 0), (0, -1), (0, 1)) # left, right, down, up
        return self.checkForContinousMoves(row, col, boardState, RookMoves)

    def getBishopMoves(self, row, col, boardState):
        BishopMoves = ((-1, -1), (1, -1), (-1, 1), (1, 1))  # left down, right down, left up, right up
        return self.checkForContinousMoves(row, col, boardState, BishopMoves)

    def getQueenMoves(self, row, col, boardState):
        QueenMoves = ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, -1), (-1, 1), (1, 1))
        return self.checkForContinousMoves(row, col, boardState, QueenMoves)

    def getKingMoves(self, row, col, boardState):

        kingMoves = ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, -1), (-1, 1), (1, 1))
        possibleMoves = []
        allyColor = boardState[row][col][0]
        enemyColor = "White" if allyColor == "Black" else "Black"
        attackedSquares = self.getAllAttacks(boardState, enemyColor)

        for move in kingMoves:
            endRow = row + move[0]
            endCol = col + move[1]
            if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                endPiece = boardState[endRow][endCol]
                if endPiece[0] != allyColor and ((endRow, endCol) not in attackedSquares):
                    possibleMoves.append((endRow, endCol))

        return possibleMoves

    def isCheck(self, boardState, color):
        enemyColor = "White" if color == "Black" else "Black"
        for indexY, row in enumerate(boardState):
            for indexX, tile in enumerate(row):
                if tile[0] == color and tile[1] == "King":
                    kingPos = (indexY, indexX)
                    break

        if kingPos in self.getAllAttacks(boardState, enemyColor):
            return True

    def checkForPins(self, col, row, boardState):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        possiblePins = ()
        allyColor = boardState[row][col][0]

        #Check for rooks/queens
        RookMoves = ((-1, 0), (1, 0), (0, -1), (0, 1))

        #Check for bishops/quuens

        #Check for pawns

        #Check for Knights

        #Check for Kings

    def checkForContinousMoves(self, row, col, boardState, setOfMoves):
        possibleMoves = []
        allyColor = boardState[row][col][0]
        enemyColor = "White" if allyColor == "Black" else "Black"

        for move in setOfMoves:
            nextRow = row
            nextCol = col
            while True:
                nextRow += move[0]
                nextCol += move[1]
                if 0 <= nextRow <= 7 and 0 <= nextCol <= 7:
                    nextSquare = boardState[nextRow][nextCol]
                    if nextSquare[0] == enemyColor:  # Its enemy piece
                        possibleMoves.append((nextRow, nextCol))
                        break
                    elif nextSquare[0] != allyColor:  # Its Empty square
                        possibleMoves.append((nextRow, nextCol))
                    else:
                        break
                else:
                    break

        return possibleMoves

