# thuis calss is responsible for storing all the info aboyut current state of chess agame
#  also responsible for determing the valid moves at the currnt sate also keep move loogs
# it will also kep the move log 

class GameState():
    def __init__(self):
        # board is 8*8 3d list each element of the list has 2 charactors first charactor represent represent the color of the list second charactorr represent the type of the list
        #  "--" represent empty space
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]  
        ]
        self.moveFunctions={'p':self.getPawnMoves,'R':self.getRookMoves,
                            'B':self.getBishopMoves,'N':self.getKnightMoves,
                            'Q':self.getQueenMoves,'K':self.getKingMoves}
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7,4)
        self.blackkingLocation = (0,4) 
        self.checkMate = False
        self.staleMate = False
        self.empassantPossible = () #coordingate or square where empassone capture is possible
        self.currentCastelRights = CastelRights(True,True,True,True)
        self.castelRightsLog = [CastelRights(self.currentCastelRights.wks,self.currentCastelRights.bks,self.currentCastelRights.wqs,self.currentCastelRights.bqs)]
    ''' 
    takes a move as parameter and execue will not work in case of casetling , pawn promotion , en pesant 
    ''' 
    def makeMove(self,move):
        self.board[move.startRow][move.startCol]="--" 
        self.board[move.endRow][move.endCol]=move.pieceMoved
        self.moveLog.append(move) #log the meove so that we can undo the move or we can show the hitory
        self.whiteToMove = not self.whiteToMove
        # update the king locationif movesd 
        if move.pieceMoved == "wK":
            self.whiteKingLocation=(move.endRow,move.endCol)
        elif move.pieceMoved == "bK":
            self.blackkingLocation=(move.endRow,move.endCol)

        # pawn promotiopn
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol]=move.pieceMoved[0]+'Q'
        
        # empasant move
        if move.isEmpassantMove:
            self.board[move.startRow][move.endCol] = '--' # capture th pawn maybe opponent one

        # updaete the empassant move possible
        if move.pieceMoved[1]=='p'and abs(move.startRow - move.endRow) == 2: #only on 2 square pawn advances
            self.empassantPossible=((move.startRow+move.endRow)//2,move.startCol)
        else: 
            self.empassantPossible = ()

        # castel move
        if move.isCastelMove:
            if move.endCol - move.startCol ==2: #king sidecastel
                #mkinbg is aulredfy moveing up
                #move rook
                self.board[move.endRow][move.endCol-1] = self.board[move.endRow][move.endCol+1]
                self.board[move.endRow][move.endCol+1] = '--' #erase the old rook
            else: #queen side castel
                self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-2] #move the rook
                self.board[move.endRow][move.endCol-2] = '--'
        #update the casteling rights whenever it is rook or king move 
        self.updateCastelingRights(move)
        self.castelRightsLog.append(CastelRights(self.currentCastelRights.wks,self.currentCastelRights.bks,self.currentCastelRights.wqs,self.currentCastelRights.bqs))
        
    '''
    undo last move
    '''
    def undoMove(self):
        if len(self.moveLog)!=0:
            move = self.moveLog.pop() 
            self.board[move.startRow][move.startCol] = move.pieceMoved 
            self.board[move.endRow][move.endCol] = move.pieceCapture  
            self.whiteToMove = not self.whiteToMove #switch turn back
            # update the king locationif movesd 
            if move.pieceMoved == "wK":
                self.whiteKingLocation=(move.startRow,move.startCol)
            elif move.pieceMoved == "bK":
                self.blackkingLocation=(move.startRow,move.startCol)

            # undo empassent move
            if move.isEmpassantMove:
                self.board[move.endRow][move.endCol] = '--' # we leave the landing square blank
                self.board[move.startRow][move.endCol]=move.pieceCapture
                self.empassantPossible = (move.endRow,move.endCol)

            # undo a 2 square pawn advance
            if move.pieceMoved[1]=='p' and abs(move.startRow-move.endRow)==2:
                self.empassantPossible = ()

            # undo castel rights 
            self.castelRightsLog.pop() #get rid of new asre rights form the move we are undoing 
            rights = self.castelRightsLog[-1]
            self.currentCastelRights = CastelRights(rights.wks, rights.bks, rights.wqs, rights.bqs)

            #undo the castel nmove
            if move.isCastelMove:
                if move.endCol - move.startCol ==2: #king side
                    self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-1] 
                    self.board[move.endRow][move.endCol-1] = '--'
                else:
                    self.board[move.endRow][move.endCol-2] = self.board[move.endRow][move.endCol+1] 
                    self.board[move.endRow][move.endCol+1] = '--'
                   
           
        # self.whiteToMove = not self.whiteToMove
        # prev_move = self.moveLog[len(self.moveLog)-1]
        # self.board[prev_move.endRow][prev_move.endCol]=prev_move.pieceCapture
        # self.board[prev_move.startRow][prev_move.startCol]= prev_move.pieceMoved

    def updateCastelingRights(self, move):
        if move.pieceMoved == "wK":
            self.currentCastelRights.wks = False
            self.currentCastelRights.wqs = False
        if move.pieceMoved == "bK":
            self.currentCastelRights.bks = False
            self.currentCastelRights.bqs = False
        if move.pieceMoved == "wR":
            if move.startRow == 7:
                if move.startCol == 0: #left side 
                    self.currentCastelRights.wqs=False
                elif move.startCol== 7:
                    self.currentCastelRights.wks=False
        if move.pieceMoved == "bR":
            if move.startRow == 0:
                if move.startCol == 0: #left side 
                    self.currentCastelRights.bqs=False
                elif move.startCol== 7:
                    self.currentCastelRights.bks=False
    
    
    '''
    All moves considering checks
    '''
    def getValidMoves(self):
        tempEmpassantPossible = self.empassantPossible
        tempCastelRights = CastelRights(self.currentCastelRights.wks,self.currentCastelRights.bks,self.currentCastelRights.wqs,self.currentCastelRights.bqs)
        # 1. generate all possible moves
        moves = self.getAllPossibleMoves()
        if self.whiteToMove:
            self.getCastelMoves(self.whiteKingLocation[0],self.whiteKingLocation[1],moves)
        else:
            self.getCastelMoves(self.blackkingLocation[0],self.blackkingLocation[1],moves)
        # 2. for each move make the move
        for i in range(len(moves)-1,-1,-1): #when removing from the list go backwords the list
            self.makeMove(moves[i])
            # 3. generate all opponets move
            # 4. for each of your opponets move see if they attack your king
            self.whiteToMove = not self.whiteToMove  # because make move switch the turns 
            a= self.isCheck()
            if a==True: # 5. if they do attackyour king then not a valid move
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        # there are more efficient algorithms exist but this is the most easiest one nad the less efficient one
        if len(moves)==0:  # either checkmate or stale mate 
            self.checkMate = True
            self.staleMate=True
        else:
            self.checkMate=False
            self.staleMate=False
        self.empassantPossible = tempEmpassantPossible  # we dont want to change thingsa as we check do the things !!!!
        self.currentCastelRights = tempCastelRights
        return moves

    ''' determine if the current player is under check'''

    def isCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0],self.whiteKingLocation[1])
        else: 
            return self.squareUnderAttack(self.blackkingLocation[0],self.blackkingLocation[1])

    '''determine if enemy can attack the square r c '''

    def squareUnderAttack(self,r,c):
        self.whiteToMove = not self.whiteToMove  #switch to opponent moves
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        for i in oppMoves:
            if(i.endRow==r and i.endCol ==c):
                return True
        return False
    '''
    All moves without considering checks
    '''
    def getAllPossibleMoves(self):
        moves=[]
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn=='w' and self.whiteToMove) or (turn=='b' and not self.whiteToMove):
                    piece = self.board[r][c][1] 
                    self.moveFunctions[piece](r,c,moves) #call approperate functions
        return moves

    '''get all the possible pawn moves for the pawn located at the row and col and add these move to the list named moves tha is been passed'''

    def getPawnMoves(self,r,c,moves):
        if self.whiteToMove: # white pawn moves
            if(r-1>=0 and self.board[r-1][c]=="--"):
                moves.append(Move((r,c),(r-1,c),self.board)) 
                if(r==6 and self.board[r-2][c]=="--"):
                    moves.append(Move((r,c),(r-2,c),self.board)) 

            if c-1>=0: #capture to the left
                if(self.board[r-1][c-1][0]=='b'):
                    moves.append(Move((r,c),(r-1,c-1),self.board))
                elif (r-1,c-1) == self.empassantPossible:
                    moves.append(Move((r,c),(r-1,c-1),self.board,isEmpassantMove = True))
            if c+1<=7: #capture to the right
                if(self.board[r-1][c+1][0]=='b'):
                    moves.append(Move((r,c),(r-1,c+1),self.board))
                elif (r-1,c+1) == self.empassantPossible:
                    moves.append(Move((r,c),(r-1,c+1),self.board,isEmpassantMove = True))
        else:
            if(r+1<=7 and self.board[r+1][c]=="--"):
                moves.append(Move((r,c),(r+1,c),self.board)) 
                if(r==1 and self.board[r+2][c]=="--"):
                    moves.append(Move((r,c),(r+2,c),self.board))
            if c-1>=0: #capture to the left
                if(r+1<=7 and self.board[r+1][c-1][0]=='w'):
                    moves.append(Move((r,c),(r+1,c-1),self.board))
                elif (r+1,c-1) == self.empassantPossible:
                    moves.append(Move((r,c),(r+1,c-1),self.board,isEmpassantMove = True))
            if c+1<=7: #capture to the right
                if(r+1<=7 and self.board[r+1][c+1][0]=='w'):
                    moves.append(Move((r,c),(r+1,c+1),self.board))
                elif (r+1,c+1) == self.empassantPossible:
                    moves.append(Move((r,c),(r+1,c+1),self.board,isEmpassantMove = True))


    '''get all the possible rook moves for the rook located at the row and col and add these move to the list named moves tha is been passed'''

    def getRookMoves(self,r,c,moves):
        enemy='w'
        if self.whiteToMove:
            enemy = 'b'
        for i in range(r+1,8):
            if self.board[i][c]=="--":
                moves.append(Move((r,c),(i,c),self.board))
            elif self.board[i][c][0]==enemy:
                moves.append(Move((r,c),(i,c),self.board))
                break
            elif self.board[i][c][0]!=enemy:
                break
        for i in range(r-1,-1,-1):
            if self.board[i][c]=="--":
                moves.append(Move((r,c),(i,c),self.board))
            elif self.board[i][c][0]==enemy:
                moves.append(Move((r,c),(i,c),self.board))
                break
            elif self.board[i][c][0]!=enemy:
                break
        for i in range(c+1,8):
            if self.board[r][i]=="--":
                moves.append(Move((r,c),(r,i),self.board))
            elif self.board[r][i][0]==enemy:
                moves.append(Move((r,c),(r,i),self.board))
                break
            elif self.board[r][i][0]!=enemy:
                break
        for i in range(c-1,-1,-1):
            if self.board[r][i]=="--":
                moves.append(Move((r,c),(r,i),self.board))
            elif self.board[r][i][0]==enemy:
                moves.append(Move((r,c),(r,i),self.board))
                break
            elif self.board[r][i][0]!=enemy:
                break

    def getBishopMoves(self,r,c,moves):
        enemy='w'
        if self.whiteToMove:
            enemy='b'       
        i=r+1
        j=c+1
        while i<8 and j<8 and i>=0 and j>=0:
            if self.board[i][j]=="--":
                moves.append(Move((r,c),(i,j),self.board))
            elif self.board[i][j][0]==enemy:
                moves.append(Move((r,c),(i,j),self.board))
                break
            else:
                break
            i=i+1
            j=j+1
        i=r-1
        j=c+1
        while i<8 and j<8 and i>=0 and j>=0:
            if self.board[i][j]=="--":
                moves.append(Move((r,c),(i,j),self.board))
            elif self.board[i][j][0]==enemy:
                moves.append(Move((r,c),(i,j),self.board))
                break
            else:
                break
            i=i-1
            j=j+1
        i=r+1
        j=c-1
        while i<8 and j<8 and i>=0 and j>=0:
            if self.board[i][j]=="--":
                moves.append(Move((r,c),(i,j),self.board))
            elif self.board[i][j][0]==enemy:
                moves.append(Move((r,c),(i,j),self.board))
                break
            else:
                break
            i=i+1
            j=j-1
        i=r-1
        j=c-1
        while i<8 and j<8 and i>=0 and j>=0:
            if self.board[i][j]=="--":
                moves.append(Move((r,c),(i,j),self.board))
            elif self.board[i][j][0]==enemy:
                moves.append(Move((r,c),(i,j),self.board))
                break
            else:
                break
            i=i-1
            j=j-1


    def getKnightMoves(self,r,c,moves):
        knightMoves = ((-2,-1), (-2,1), (-1,-2), (-1,2), (1,-2), (1,2), (2,-1), (2,1))
        allyColor = "w" if self.whiteToMove else "b"
        for m in knightMoves:
            endRow = r+m[0]
            endCol = c+m[1]
            if 0<=endRow<8 and 0<=endCol<8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0]!=allyColor:
                    moves.append(Move((r,c),(endRow,endCol),self.board))



    def getQueenMoves(self,r,c,moves):
        self.getRookMoves(r,c,moves) 
        self.getBishopMoves(r,c,moves) 


    # def getKingMoves(self,r,c,moves):
    #     ally = 'b'
    #     if self.whiteToMove:
    #         ally = 'w'
    #     if(r+1<8 and self.board[r+1][c][0] !=ally ):
    #         moves.append(Move((r,c),(r+1,c),self.board))
    #         if(c+1<8 and self.board[r+1][c+1][0] !=ally):
    #             moves.append(Move((r,c),(r+1,c+1),self.board))
    #         if(c-1>=0 and self.board[r+1][c-1][0] !=ally):
    #             moves.append(Move((r,c),(r+1,c-1),self.board))
    #     if(r-1>=0 and self.board[r-1][c][0] !=ally):
    #         moves.append(Move((r,c),(r-1,c),self.board))
    #         if(c+1<8 and self.board[r-1][c+1][0] !=ally):
    #             moves.append(Move((r,c),(r-1,c+1),self.board))
    #         if(c-1>=0 and self.board[r-1][c-1][0] !=ally):
    #             moves.append(Move((r,c),(r-1,c-1),self.board))
    #     if(c+1<8 and self.board[r][c+1][0] !=ally):
    #         moves.append(Move((r,c),(r,c+1),self.board))
    #     if(c-1>=0 and self.board[r][c-1][0] !=ally):
    #         moves.append(Move((r,c),(r,c-1),self.board))  
    def getKingMoves(self, r, c, moves):
        ally = 'w' if self.whiteToMove else 'b'
        directions = [(-1, -1), (-1, 0), (-1, 1),
                    (0, -1),           (0, 1),
                    (1, -1),  (1, 0),  (1, 1)]
        
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < 8 and 0 <= nc < 8:
                if self.board[nr][nc][0] != ally:
                    moves.append(Move((r, c), (nr, nc), self.board))
        

    def getCastelMoves(self,r,c,moves,):
        if self.squareUnderAttack(r,c):
            return
        if (self.whiteToMove and self.currentCastelRights.wks==True) or (not self.whiteToMove and self.currentCastelRights.bks==True) :
            self.getKingSideCastelMoves(r,c,moves)
        if (self.whiteToMove and self.currentCastelRights.wqs==True) or (not self.whiteToMove and self.currentCastelRights.bqs==True) :
            self.getQueenSideCastelMoves(r,c,moves)
        
    def getKingSideCastelMoves(self,r,c,moves):
        if self.board[r][c+1] == '--' and self.board[r][c+2] == '--':
            if not self.squareUnderAttack(r,c+1) and not self.squareUnderAttack(r,c+2): 
                moves.append(Move((r,c),(r,c+2),self.board,isCastelMove=True))

    def getQueenSideCastelMoves(self,r,c,moves):
        if self.board[r][c-1]=='--' and self.board[r][c-2]=='--' and self.board[r][c-3]=='--' :
            if not self.squareUnderAttack(r,c-1) and not self.squareUnderAttack(r,c-2) and not self.squareUnderAttack(r,c-3):
                moves.append(Move((r,c),(r,c-2),self.board,isCastelMove=True))



class CastelRights():
    def __init__(self , wks, bks,wqs,bqs): #black king side , white king side , black queen side etc
        self.wks = wks 
        self.bks = bks 
        self.wqs = wqs 
        self.bqs = bqs



class Move():
    #map key to value 
    # key : value
    rankToRows = {"1":7,"2":6,"3":5,"4":4,
                  "5":3,"6":2,"7":1,"8":0}
    rowsToRank = {v:k for k ,v in rankToRows.items()}
    filesTocols={"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7}
    colToFiles = {v:k for k,v in filesTocols.items()}

    def __init__(self,startsq,endsq,board, isEmpassantMove =False, isCastelMove = False):
        self.startRow = startsq[0]
        self.startCol = startsq[1]
        self.endRow = endsq[0]
        self.endCol = endsq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCapture = board[self.endRow][self.endCol]
        self.isPawnPromotion = False
         
        if (self.pieceMoved == 'wp' and self.endRow==0) or (self.pieceMoved=='bp' and self.endRow==7):
            self.isPawnPromotion = True
        # empassant stuff
       
        
        self.isEmpassantMove = isEmpassantMove
        if self.isEmpassantMove:
            self.pieceCapture = 'wp' if self.pieceMoved=='bp' else 'bp'

        # castling stuff
        self.isCastelMove =isCastelMove
        self.moveID = self.startRow*1000 + self.startCol*100 + self.endRow*10 + self.endCol 
        # print(self.moveID)

    '''
    overiding the equal method : actually the move object is same means in valid move
    list as we checkthatcurrent Move object is in Valid move object or not
    '''
    def __eq__(self, other): #comparing one object to anothr object
        if isinstance(other , Move): # its a good practice just check that if the pssing Move obj is instance of this class or not.
            return self.moveID == other.moveID
        return False 

    def getChessNotation(self):
        # you can add this to maek a real chess notation 
        return self.getRankFile(self.startRow,self.startCol) + self.getRankFile(self.endRow,self.endCol) 

    def getRankFile(self,r,c):
        return self.colToFiles[c] + self.rowsToRank[r]


