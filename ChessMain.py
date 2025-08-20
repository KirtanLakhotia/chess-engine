# this is our main driver it will be reaponsible for the user inputs and displaying the current game states etc 
import pygame as p
import ChessEngine
import smartMoveFinder
# p.init() it is good to inoitilize above because if somethiung is dependent on p i the load fn  thn it wll give error 
WEIDTH=HEIGHT=512  #400 IS ANOTHER GOOD OPTION
DIMENSIONS = 8  #dinmension of the board is 8*8
SQ_SIZE = HEIGHT//DIMENSIONS
MAX_FPS = 15 #for animation later on 
IMAGES= {}

'''
initilize a global dictionary of images this will be called exactly once in the main
'''

def loadImages():
    pieces= ['wp','wR','wN','wB','wK','wQ','bp','bR','bN','bB','bK','bQ',] 
    for piece in pieces:
        IMAGES[piece]=p.transform.scale(p.image.load("./images/"+piece+".png"),(SQ_SIZE,SQ_SIZE) )
    # note we can access the image by saying IMAGES['wp'] because the fn will once called and then the things will e stored oin the global variable 

'''
this will be our main driver this wll handle user input and updating the graphics
'''

def main():
    p.init()
    screen = p.display.set_mode((WEIDTH,HEIGHT))
    Clock = p.time.Clock()
    screen.fill(p.Color("white")) 
    gs = ChessEngine.GameState()
    print(gs.board) 
    validMoves = gs.getValidMoves()  #its an function actually
    moveMade = False #flag variable for when a move is made until the moveis made we shpuld not regenerate the valid moves
    animate= False #flag variable for whenwe shpuld animate
    loadImages() # we are going to only od this once befor the while loop
    running = True 
    sqSelected =() # no square is selected initially it will be tupple : (row,col)
    playerClicks=[] #keeptrack of player clicks two tupples[(6,4),(4,4)]
    gameOver=False
    playerOne=True #if human is playing white then it will be true. If an AI isplaying the False
    playerTwo=False #same as above but for black
    while running:
        humanTurn = (gs.whiteToMove and  playerOne) or (not gs.whiteToMove and playerTwo)
        for e in p.event.get():
            if e.type == p.quit:
                running = False
            #mouse handler 
            elif e.type==p.MOUSEBUTTONDOWN:
                if not gameOver and humanTurn:
                    location = p.mouse.get_pos() #(x,y) location of mouse
                    col = location[0]//SQ_SIZE 
                    row = location[1]//SQ_SIZE
                    if sqSelected == (row,col): #the user click the sam twice
                        sqSelected=()
                        playerClicks=[] #clear player clicks
                    else:
                        sqSelected=(row,col)
                        # print(sqSelected)
                        playerClicks.append(sqSelected) #appen for both first and second click

                    # if sqSelected == (row,col): #doinf for click parity clicking on diff then only get the access to move 
                    #     prev_row = sqSelected[0]
                    #     prev_col = sqSelected[1]
                    #     if(gs.board[prev_row][prev_col][0]==gs.board[row][col][0]):
                    #         playerClicks=[]
                    #         playerClicks.append(sqSelected)
                    #         sqSelected=(row,col)

                    if len(playerClicks)==2: #after the second click
                        move = ChessEngine.Move(playerClicks[0],playerClicks[1],gs.board)
                        print(move.getChessNotation())
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                moveMade=True 
                                animate=True 
                                sqSelected=() #reset the clicks
                                playerClicks=[]
                        if not moveMade:
                            playerClicks=[sqSelected]
            #key handler
            elif e.type == p.KEYDOWN:
                if e.key ==  p.K_z: #undo when z is pressed
                    gs.undoMove()
                    # validMoves = gs.getValidMoves()
                    animate=False
                    moveMade = True 

                if e.key ==  p.K_r: #reset when r is pressed
                    gs=ChessEngine.GameState()
                    validMoves=gs.getValidMoves()
                    sqSelected=()
                    playerClicks=[]
                    animate=False
                    moveMade = False 
        
        #AI movefinder logic
        if not gameOver and not humanTurn:
            AIMove = smartMoveFinder.findBestMove(gs,validMoves)
            if AIMove is None:
                AIMove = smartMoveFinder.findRandomMove(gs,validMoves)
            gs.makeMove(AIMove)
            moveMade=True
            animate=True

        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1],screen,gs.board,Clock)
            validMoves = gs.getValidMoves()
            moveMade=False
        drawGameState(screen,gs,sqSelected,validMoves) 
        if gs.checkMate==True:
            gameOver=True
            if gs.whiteToMove:
                drawText(screen,'Black win by checkmate')
            else:
                drawText(screen,'White win by checkmate')
        elif gs.staleMate:
            gameOver=True
            drawText(screen,'StaleMate')
        
        Clock.tick(MAX_FPS)
        p.display.flip()
 

'''
highlisht the square sealected and the move for piece sealected 
'''

def heilightSquares(screen,sqSelected,gs,validMoves):
    if(sqSelected!=()):
        r= sqSelected[0]
        c=sqSelected[1]
        whichMove= 'w' if gs.whiteToMove else 'b'
        if(gs.board[r][c][0]==whichMove):
            s=p.Surface((SQ_SIZE,SQ_SIZE))
            s.set_alpha(100) #transparent value 0 transparent 255 opaque
            s.fill(p.Color('blue'))
            screen.blit(s,(c*SQ_SIZE,r*SQ_SIZE)) #heilight selected square
            #heilight the moves possible squares
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if r==move.startRow and c == move.startCol:
                    screen.blit(s,(move.endCol*SQ_SIZE,move.endRow*SQ_SIZE)) #heilight selected square



'''
responsible for all the graphics on the current game
'''
def drawGameState(screen,gs,sqSelected,validMoves):
    drawBoard(screen) #this will draw the board
    heilightSquares(screen,sqSelected,gs,validMoves)
    drawPieces(screen,gs.board)

'''
it will draw the ssquares
'''
def drawBoard(screen):
    global colors
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSIONS):
        for c in range(DIMENSIONS):
            color = colors[(r+c)%2]
            p.draw.rect(screen,color,p.Rect(r*SQ_SIZE,c*SQ_SIZE,SQ_SIZE,SQ_SIZE))

'''
draw the pieceson the board the images we have in the folder
'''
def drawPieces(screen,board):
    for r in range(DIMENSIONS):
        for c in range(DIMENSIONS):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece],p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))


def animateMove(move,screen,board,clock):
    global colors
    dR=move.endRow-move.startRow
    dC=move.endCol-move.startCol
    framesPerSquare = 10 
    frameCount = (abs(dR)+abs(dC))* framesPerSquare
    for frame in range(frameCount+1):
        r,c = (move.startRow+dR*frame/frameCount,move.startCol+dC*frame/frameCount)
        drawBoard(screen)
        drawPieces(screen,board)
        #erase the piece moved from its ending position
        color= colors[(move.endRow+move.endCol)%2]
        endSquare = p.Rect(move.endCol*SQ_SIZE,move.endRow*SQ_SIZE,SQ_SIZE,SQ_SIZE)
        p.draw.rect(screen,color,endSquare)
        #draw captured piece into rectangle
        if move.pieceCapture != '--':
            screen.blit(IMAGES[move.pieceCapture],endSquare)

        #draw moving piece
        screen.blit(IMAGES[move.pieceMoved],p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))
        p.display.flip()
        clock.tick(60)


def drawText(screen,text):
    font = p.font.SysFont("Helvitica",32,True,False)
    textObject = font.render(text,0,p.Color('Grey'))
    textLocation = p.Rect(0,0,WEIDTH,HEIGHT).move(WEIDTH/2-textObject.get_width()/2,HEIGHT/2-textObject.get_height()/2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text,0,p.Color('Black'))
    screen.blit(textObject, textLocation.move(2,2))


# main() we can do this also 

if __name__ == "__main__":
    main() # as much i know this will only run if i am running this python file and in this file only the main is ther    