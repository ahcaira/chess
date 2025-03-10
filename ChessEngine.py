class GameState():
    def __init__(self):
        self.board = [
            ['bRR', 'bRN', 'bRB', 'bRQ', 'bRK', 'bRB', 'bRN', 'bRR'],
            ['bRp', 'bRp', 'bRp', 'bRp', 'bRp', 'bRp', 'bRp', 'bRp'],
            ['---', '---', '---', '---', '---', '---', '---', '---'],
            ['---', '---', '---', '---', '---', '---', '---', '---'],
            ['---', '---', '---', '---', '---', '---', '---', '---'],
            ['---', '---', '---', '---', '---', '---', '---', '---'],
            ['wRp', 'wRp', 'wRp', 'wRp', 'wRp', 'wRp', 'wRp', 'wRp'],
            ['wRR', 'wRN', 'wRB', 'wRQ', 'wRK', 'wRB', 'wRN', 'wRR']]
        self.whiteToMove = True
        self.moveLog = []