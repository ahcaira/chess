import pygame as p
import engine

WIDTH = HEIGHT = 512
DIMENSIONS = 8
SQ_SIZE = HEIGHT // DIMENSIONS
MAX_FPS = 15
IMAGES = {}

# load images beforehand because it's costly
def loadImages():
    pieces = {'wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ'}

    # draw image as IMAGES['wp']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

def main():
    # never a bad idea to put p.init() in front
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = engine.GameState()
    validMoves = gs.getValidMoves()
    print('moves below')
    for move_ in validMoves:
        print(move_.startRow, move_.startCol, move_.endRow, move_.endCol)
    #print(validMoves[0)
    moveMade = False

    loadImages()

    running = True
    sqSelected = ()
    playerClicks = []
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # Mouse
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sqSelected == (row, col):
                    sqSelected = () # deselect
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)
                if len(playerClicks)== 2:
                    move = engine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                        sqSelected = ()
                        playerClicks = []
                    else:
                        playerClicks = [sqSelected]
            # Keyboard
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True

        if moveMade:
            validMoves = gs.getValidMoves()
            print('moves below')
            for move_ in validMoves:
                print(move_.startRow, move_.startCol, move_.endRow, move_.endCol)
            moveMade = False


        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)


def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for i in range(DIMENSIONS):
        for j in range(DIMENSIONS):
            color = colors[(i + j) % 2]
            p.draw.rect(screen, color, p.Rect(i * SQ_SIZE, j * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawPieces(screen, board):
    for i in range(DIMENSIONS):
        for j in range(DIMENSIONS):
            piece = board[i][j]
            if piece != '--':
                screen.blit(IMAGES[piece], p.Rect(j * SQ_SIZE, i * SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == "__main__":
    main()