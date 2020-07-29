class board:
    def __init__(self,width,height,mines):
        self.boardArray = [[None for x in range(0,width,1)]
                            for y in range(0,height,1)]
        self.fakeArray = [["?" for x in range(0,width,1)]
                            for y in range(0,height,1)]
        self.width = width
        self.height = height
        self.mines = mines
