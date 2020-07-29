from entities.board import board
from logic.spaceCreator import spaceCreator
import os
import time
from pynput import keyboard

class gameLogic:
    def __init__(self):
        self.board = None
        self.availableDificulties = [
            "easy",
            "medium",
            "hard"
        ]

        self.boardSizes = {
            "easy": (8,8,10),
            "medium": (10,10,20),
            "hard": (20,20,100)
        }

        self.neighbour_map = [(0,-1),(0,1),(-1,-1),(-1,0),(-1,1),(1,-1),(1,0),(1,1)]

        self.gameover = False
        self.won = False
        self.flaggedMines = []
        self.uncovered_spaces = 0
        self.x = 0
        self.y = 0
        self.clear = lambda: os.system('cls' if os.name=='nt' else 'clear')

    def startGame(self):
        print("Minesweeper")
        print("Choose game difficulty:")
        for i in range(len(self.availableDificulties)):
            print(str(i+1)+"."+self.availableDificulties[i])
        if self.selectedDifficulty(input())==False:
            self.startGame()
        else:
            listener = keyboard.Listener(on_press=self.__keyboard_listener,suppress=True)
            listener.start()
            while(self.gameover==False):
                self.clear()
                self.__print_board(self.board.fakeArray)
                self.__print_controls()
                time.sleep(.500)
                self.clear()
                self.__print_board(self.board.fakeArray,True)
                self.__print_controls()
                time.sleep(.500)
            listener.stop()
            if(self.gameover and self.won == False):
                self.clear()
                self.__print_board(self.board.fakeArray)
                print("Game over")
            elif(self.gameover and self.won):
                self.clear()
                self.__print_board(self.board.fakeArray)
                print("You won")
            input()




    def selectedDifficulty(self,selectedOption)->bool:
        self.clear()
        selectedOption = int(selectedOption)-1
        if selectedOption  not in range(len(self.availableDificulties)):
            return False
        else:
            selecteDificulty = self.availableDificulties[selectedOption]
            (width,height,mines)=self.boardSizes[selecteDificulty]
            print("You choosed: "+self.availableDificulties[selectedOption])
            print("This option, will create a board of {0} by {1} , with {2} mines".format(width,height,mines))
            print("Are you sure?")
            confirm = input("Yes/No:\n")
            if confirm.lower() == "yes":
                self.board = board(width,height,mines)
                space = spaceCreator(self.board)
            else:
                return False

    def __print_board(self,board, cursorBlink = False):
        for i in range(len(board)):
            row = ""
            for j in range(len(board)):
                if self.y == i and self.x == j and cursorBlink:
                    row += "\u2588"+","
                elif board[i][j] == None:
                    row += "?,"
                else:
                    row += board[i][j]+","
            print(row[0:len(row)-1])

    def __print_controls(self):
        print("Mines: "+str(self.board.mines)+"  Flags: "+str(len(self.flaggedMines)))
        print("Move with arrow keys")
        print("Press F to flag mines")
        print("Press SPACE key to uncover square")
        print("Press ESC to close game")

    def __keyboard_listener(self,key):
        if key == keyboard.Key.esc:
            self.gameover = True
        elif key == keyboard.Key.down and self.y < len(self.board.boardArray)-1:
            self.y += 1
        elif key == keyboard.Key.up and self.y > 0:
            self.y -= 1
        elif key == keyboard.Key.left and self.x > 0:
            self.x -= 1
        elif key == keyboard.Key.right and self.x < len(self.board.boardArray[self.y])-1:
            self.x += 1
        elif key == keyboard.Key.space:
            self.__uncover_spaces()
        else:
            try:
                if key.char == 'F' or key.char == 'f':
                    self.__flag_space()
                print(key)
            except AttributeError:
                print("special key {0} ".format(key))

    
    def __uncover_spaces(self):
        if(self.board.boardArray[self.y][self.x]=="*" and self.board.fakeArray[self.y][self.x]=="?"):
            self.board.fakeArray[self.y][self.x] = "*"
            self.gameover = True
        elif(self.board.boardArray[self.y][self.x]==" "):
            self.board.fakeArray[self.y][self.x] = self.board.boardArray[self.y][self.x]
            self.uncovered_spaces += 1
            self.__run_uncover_task()
        elif(self.board.boardArray[self.y][self.x] in ['1','2','3','4','5','6','7','8']):
            self.board.fakeArray[self.y][self.x] = self.board.boardArray[self.y][self.x]
            self.uncovered_spaces += 1
        self.__is_winner()

    def __run_uncover_task(self,space=None):
        for x,y in self.neighbour_map:
            new_x = (self.x if space == None else space["x"])+x 
            new_y = (self.y if space == None else space["y"])+y
            if(new_x<0 or new_y<0 or new_x>self.board.width-1 or new_y>self.board.height-1):
                continue
            if(self.board.fakeArray[new_y][new_x]=="?" and self.board.boardArray[new_y][new_x]=="*"):
                continue
            elif(self.board.fakeArray[new_y][new_x]=="?" and self.board.boardArray[new_y][new_x]==" "):
                self.board.fakeArray[new_y][new_x]=" "
                self.uncovered_spaces+=1
                self.__run_uncover_task({"x":new_x,"y":new_y})
            elif(self.board.fakeArray[new_y][new_x]=="?" and self.board.boardArray[new_y][new_x] in ['1','2','3','4','5','6','7','8']):
                self.board.fakeArray[new_y][new_x]=self.board.boardArray[new_y][new_x]
                self.uncovered_spaces+=1

    def __flag_space(self):
        if(self.board.fakeArray[self.y][self.x]=="?") and len(self.flaggedMines)<self.board.mines:
            self.board.fakeArray[self.y][self.x] = "F"
            self.flaggedMines.append((self.y,self.x))
        elif(self.board.fakeArray[self.y][self.x]=="F"):
            self.board.fakeArray[self.y][self.x] = "?"
            self.flaggedMines.remove((self.y,self.x))
        if(self.uncovered_spaces+len(self.flaggedMines) == self.board.width*self.board.height):
            self.won = True
            self.gameover = True
        self.__is_winner()

    def __is_winner(self):
        if(self.uncovered_spaces+len(self.flaggedMines) == self.board.width*self.board.height):
            self.won = True
            self.gameover = True