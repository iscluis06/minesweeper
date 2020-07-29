import random

class spaceCreator:
    def __init__(self,board):
        self.board = board
        self.initializeBoard()
    
    def initializeBoard(self):
        self.__createmines()
        self.__createIndicators()
        
    
    def __createmines(self):
        countCreatedMines  = 0
        while countCreatedMines < self.board.mines:
            width = random.randrange(0,self.board.width,1)
            height = random.randrange(0,self.board.height,1)
            if self.board.boardArray[width][height] != "*":
                self.board.boardArray[width][height] = "*"
                countCreatedMines += 1

    def __createIndicators(self):
        for x in range(0,self.board.width,1):
            row = self.board.boardArray[x]
            for y in range(0,self.board.height,1):
                if self.board.boardArray[x][y]=="*":
                    continue
                indicator = 0
                previousColumn = y-1
                previousRow = x-1
                nextRow = x+1
                nextColumn = y+1
                #check previous column
                if previousColumn>=0 and previousColumn<self.board.height and row[previousColumn]=="*":
                    indicator += 1
                #check next column
                if nextColumn>=0 and nextColumn<self.board.height and row[nextColumn]=="*":
                    indicator += 1
                #check previous row previous column
                if previousRow>= 0 and previousRow<self.board.width \
                and previousColumn>=0 and previousColumn<self.board.height \
                and self.board.boardArray[previousRow][previousColumn]=="*":
                    indicator += 1
                #check previous row same column
                if previousRow >= 0 and previousRow<self.board.width \
                and self.board.boardArray[previousRow][y]=="*":
                    indicator += 1
                #check previous row next column
                if previousRow >= 0 and previousRow<self.board.width \
                and nextColumn>=0 and nextColumn<self.board.height \
                and self.board.boardArray[previousRow][nextColumn]=="*":
                    indicator += 1
                #check next row previous column
                if nextRow >= 0 and nextRow<self.board.width \
                and previousColumn>=0 and previousColumn<self.board.height \
                and self.board.boardArray[nextRow][previousColumn]=="*":
                    indicator += 1
                #check next row same column
                if nextRow >= 0 and nextRow<self.board.width \
                and self.board.boardArray[nextRow][y]=="*":
                    indicator += 1
                #check next row next column
                if nextRow >= 0 and nextRow<self.board.width \
                and nextColumn>=0 and nextColumn<self.board.height \
                and self.board.boardArray[nextRow][nextColumn]=="*":
                    indicator += 1
                if indicator == 0:
                    self.board.boardArray[x][y] = " "
                else:
                    self.board.boardArray[x][y] = str(indicator)