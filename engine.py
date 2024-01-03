
class GameState():
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", 'bN', 'bR'],
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', 'wB', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
            ["wR", "wN", "wB", "wQ", "wK", "wB", 'wN', 'wR'],
        ]
        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                              'B': self.getBishopMoves, 'K': self.getKingMoves, 'Q': self.getQueenMoves}

        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.inCheck = False
        self.pins = []
        self.checks = []

    # TODO: castling and en-passant
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = '--'
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove

        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)


    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove


    # w/ considering checks
    def getValidMoves(self) -> [[]]:
        moves = []
        self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()
        #print('[+]')
        #print('pins', self.pins)
        #for pin in self.pins:
        #     print(pins)
        #    print(pin[0], pin[1], pin[2], pin[3])
        if self.whiteToMove:
            kingRow = self.whiteKingLocation[0]
            kingCol = self.whiteKingLocation[1]
        else:
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]
        print('kng', kingRow, kingCol)
        #print(self.inCheck)
        if self.inCheck:
            if len(self.checks) == 1:
                moves = self.getAllPossibleMoves()
                # block check
                print('trying to block check')
                check = self.checks[0]
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol]
                validSquares = []

                if pieceChecking == 'N':
                    validSquares = [[checkRow, checkCol]]
                else:
                    for i in range(1, 8):
                        validSquare = [kingRow + check[2] * i, kingCol + check[3] * i]
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[1] == checkCol:
                            break
                for square in validSquares:
                    print(square)
                #print(validSquares)

                for i in range(len(moves) - 1, -1, -1): # go backwards if you want to delete smth
                    if moves[i].pieceMoved[1] != 'K':
                        print(moves[i].startRow, moves[i].startCol, moves[i].endRow, moves[i].endCol)
                        if not [moves[i].endRow, moves[i].endCol] in validSquares:
                            moves.remove(moves[i])
            else: # double check, king has to move
                print('double check!')
                self.getKingMoves(kingRow, kingCol, moves)
        else:
            moves = self.getAllPossibleMoves()

        return moves


    def checkForPinsAndChecks(self):
        pins = []
        checks = []
        inCheck = False
        if self.whiteToMove:
            enemyColor = 'b'
            allyColor = 'w'
            startRow = self.whiteKingLocation[0]
            startCol = self.whiteKingLocation[1]
        else:
            enemyColor = 'w'
            allyColor = 'b'
            startRow = self.blackKingLocation[0]
            startCol = self.blackKingLocation[1]
        #print(allyColor)
        dirs = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, 1], [-1, -1], [1, -1]]
        for j in range(len(dirs)):
            d = dirs[j]
            possiblePin = ()
            for i in range(1, 8):
                endRow = startRow + d[0] * i
                endCol = startCol + d[1] * i

                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    #print([endRow, endCol])
                    endPiece = self.board[endRow][endCol]
                    #print(endPiece)
                    if endPiece[0] == allyColor and endPiece[1] != 'K':
                        if possiblePin == ():
                            possiblePin = (endRow, endCol, d[0], d[1])
                        else:
                            break
                    elif endPiece[0] == enemyColor:
                        #print('got her')
                        type = endPiece[1]

                        if  (0 <= j <= 3 and type == 'R') or \
                            (4 <= j <= 7 and type == 'B') or \
                            (i == 1 and type == 'p' and
                                ((enemyColor == 'w' and 6 <= j <= 7) or (enemyColor == 'b' and 4 <= j <= 5))) or \
                                (type == 'Q') or (i == 1 and type == 'K'):
                            if possiblePin == ():
                                print('got check!')
                                print(endRow,endCol,d[0],d[1]),
                                inCheck = True
                                checks.append((endRow, endCol, d[0], d[1]))
                                break
                            else:
                                #print('got pin!')
                                #print('ij', i, j, type)
                                #print(possiblePin)
                                pins.append(possiblePin)
                                break
                        else: # enemy piece not applying check
                            break
                else:
                    break

        knight_dirs = [[-1, -2], [-2, -1], [1, 2], [2, 1], [1, -2], [-1, 2], [2, -1], [-2, 1]]
        for m in knight_dirs:
            endRow, endCol = startRow + m[0], startCol + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor and endPiece[1] == 'N':
                    inCheck = True
                    checks.append((endRow, endCol, m[0], m[1]))
        return inCheck, pins, checks


    # w/o considering checks
    def getAllPossibleMoves(self):
        moves = []
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                turn = self.board[i][j][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[i][j][1]
                    self.moveFunctions[piece](i, j, moves)
        return moves

    def getPawnMoves(self, i, j, moves):
        # TODO: pawn promotions
        piecePinned = False
        pinDirection = ()
        for k in range(len(self.pins)-1, -1, -1):
            if self.pins[k][0] == i and self.pins[k][1] == j:
                piecePinned = True
                pinDirection = (self.pins[k][2], self.pins[k][3])
                self.pins.remove(self.pins[k])
                break

        if self.whiteToMove:
            if self.board[i-1][j] == "--":
                if not piecePinned or pinDirection == (-1, 0):
                    moves.append(Move((i, j), (i-1, j), self.board))
                    if i == 6 and self.board[i-2][j] == "--":
                        moves.append(Move((i, j), (i-2, j), self.board))
            if j - 1 >= 0:
                if self.board[i-1][j-1][0] == 'b':
                    if not piecePinned or pinDirection == (-1, -1):
                        moves.append(Move((i, j), (i-1, j-1), self.board))
            if j + 1 <= 7:
                if self.board[i-1][j+1][0] == 'b':
                    if not piecePinned or pinDirection == (-1, 1):
                        moves.append(Move((i, j), (i-1, j+1), self.board))
        else:
            if self.board[i+1][j] == "--":
                if not piecePinned or pinDirection == (1, 0):
                    moves.append(Move((i, j), (i+1, j), self.board))
                    if i == 1 and self.board[i+2][j] == "--":
                        moves.append(Move((i, j), (i+2, j), self.board))
            if j - 1 >= 0:
                if not piecePinned or pinDirection == (1, -1):
                    if self.board[i+1][j-1][0] == 'w':
                        moves.append(Move((i, j), (i+1, j-1), self.board))
            if j + 1 <= 7:
                if not piecePinned or pinDirection == (1, 1):
                    if self.board[i+1][j+1][0] == 'w':
                        moves.append(Move((i, j), (i+1, j+1), self.board))


    def getRookMoves(self, i, j, moves):
        piecePinned = False
        pinDirection = ()
        for k in range(len(self.pins) - 1, -1, -1):
            if self.pins[k][0] == i and self.pins[k][1] == j:
                piecePinned = True
                pinDirection = (self.pins[k][2], self.pins[k][3])
                if self.board[i][j][1] != 'Q': #can't remove queen moves here, only at bishop moves
                    self.pins.remove(self.pins[k])
                break


        dirs = [[-1, 0], [0, -1], [1, 0], [0, 1]]
        for dir in dirs:
            new_i, new_j = i, j
            while 0 <= new_i + dir[0] <= 7 and 0 <= new_j + dir[1] <= 7:
                cell = self.board[new_i + dir[0]][new_j + dir[1]]
                if not piecePinned or pinDirection == dir or pinDirection == (-dir[0], -dir[1]):
                    if cell == '--' or cell[0] != self.board[i][j][0]: # if empty or opposite color
                        moves.append(Move((i, j), (new_i + dir[0], new_j + dir[1]), self.board))
                        new_i, new_j = new_i + dir[0], new_j + dir[1]
                        if cell != '--':
                            break
                    else:
                        break
                else:
                    break

    def getKnightMoves(self, i, j, moves):
        piecePinned = False
        pinDirection = ()
        for k in range(len(self.pins) - 1, -1, -1):
            if self.pins[k][0] == i and self.pins[k][1] == j:
                piecePinned = True
                self.pins.remove(self.pins[k])
                break

        dirs = [[-1, -2], [-2, -1], [1, 2], [2, 1], [1, -2], [-1, 2], [2, -1], [-2, 1]]
        for dir in dirs:
            new_i, new_j = i + dir[0], j + dir[1]
            if 0 <= new_i <= 7 and 0 <= new_j <= 7:
                if self.board[new_i][new_j] == '--' or self.board[new_i][new_j][0] != self.board[i][j][0]:
                    if not piecePinned:
                        moves.append(Move((i, j), (new_i, new_j), self.board))


    def getBishopMoves(self, i, j, moves):
        piecePinned = False
        pinDirection = ()
        for k in range(len(self.pins) - 1, -1, -1):
            if self.pins[k][0] == i and self.pins[k][1] == j:
                piecePinned = True
                pinDirection = (self.pins[k][2], self.pins[k][3])
                self.pins.remove(self.pins[k])
                break
        dirs = [[-1, -1], [1, 1], [-1, 1], [1, -1]]
        for dir in dirs:
            new_i, new_j = i, j
            while 0 <= new_i + dir[0] <= 7 and 0 <= new_j + dir[1] <= 7:
                cell = self.board[new_i + dir[0]][new_j + dir[1]]
                if cell == '--' or cell[0] != self.board[i][j][0]:  # if empty or opposite color
                    if not piecePinned or pinDirection == dir or pinDirection == (-dir[0], -dir[1]):
                        moves.append(Move((i, j), (new_i + dir[0], new_j + dir[1]), self.board))
                        new_i, new_j = new_i + dir[0], new_j + dir[1]
                        if cell != '--':
                            break
                    else:
                        break
                else:
                    break

    def getKingMoves(self, i, j, moves):
        dirs = [[-1, -1], [1, 1], [-1, 1], [1, -1], [0, -1], [0, 1], [1, 0], [-1, 0]]
        for dir in dirs:
            new_i, new_j = i + dir[0], j + dir[1]
            if 0 <= new_i <= 7 and 0 <= new_j <= 7:
                if self.board[new_i][new_j] == '--' or self.board[new_i][new_j][0] != self.board[i][j][0]:
                    if self.board[i][j][0] == 'w':
                        self.whiteKingLocation = (new_i, new_j)
                    else:
                        self.blackKingLocation = (new_i, new_j)
                    inCheck, pins, check = self.checkForPinsAndChecks()
                    if not inCheck:
                        moves.append(Move((i, j), (new_i, new_j), self.board))
                    if self.board[i][j][0] == 'w':
                        self.whiteKingLocation = (i, j)
                    else:
                        self.blackKingLocation = (i, j)

    def getQueenMoves(self, i, j, moves):
        self.getBishopMoves(i, j, moves)
        self.getRookMoves(i, j, moves)

class Move():
    # invert values from normal to computer: "1" -> 7, "2" -> 6 etc.
    ranksToRows = {x: 8 - int(x) for x in '12345678'}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}

    # letters to numbers: "a" -> 0, "b" -> 1 etc.
    filesToCols = {'abcdefgh'[x]: x for x in range(8)}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol


    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID


    def getChessNotation(self):
        # TODO: add real chess notation (from g1f3 to Kf3)
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)


    def getRankFile(self, row, col):
        return self.colsToFiles[col] + self.rowsToRanks[row]

