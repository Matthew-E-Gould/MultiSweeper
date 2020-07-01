import numpy as np
import random
import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class Tile:

    def __init__(self):

        # Class initialisation
        self.tile_type = 0  # stores the type of tile, 0-8 = bomb adjacency, 9 = bomb
        self.flagged = False  # stores if the tile has been flagged
        self.clicked = False  # stores if the tile has been clicked
        self.bomb = False  # stores if the tile is a bomb or not

        # stores the image of the tile
        self.tile_img = QtWidgets.QLabel()
        self.tile_img.setPixmap(QtGui.QPixmap("unknown.png"))

        self.PLACEHOLDER = None  # Placeholder, remove when done

    def generate(self, value):
        self.tile_type = value  # stores the type of tile, 0-8 = bomb adjacency, 9 = bomb
        if 0 <= self.tile_type < 9:
            self.bomb = False
        elif self.tile_type == 9:
            self.bomb = True
        else:
            print("ERROR: tile_type value (" + str(self.tile_type) + ") is out of range.")  # DEBUG

    # function for what to do when the tile is left clicked
    def left_click(self):
        if not self.flagged and not self.clicked:  # makes sure that the tile has not been flagged

            self.clicked = True  # saves processing time
            if 0 <= self.tile_type < 9:  # if the tile is an adjacency tile
                self.tile_img.setPixmap(QtGui.QPixmap(str(self.tile_type)+".png"))

            elif self.tile_type == 9:  # if the tile is a bomb
                self.tile_img.setPixmap(QtGui.QPixmap("bomb.png"))

            else:
                print("ERROR: tile_type value (" + str(self.tile_type) + ") is out of range.")  # DEBUG
            return self.bomb
        return False

    # function for what to do when the tile is right clicked
    def right_click(self):
        if not self.clicked:  # makes sure that the tile has not already been clicked
            if self.flagged:
                self.tile_img.setPixmap(QtGui.QPixmap("unknown.png"))
                self.flagged = False
            else:
                self.tile_img.setPixmap(QtGui.QPixmap("flag.png"))
                self.flagged = True
        return self.flagged

    def debug_get_tile_type(self):
        return self.tile_type
# END OF TILE CLASS ####################################################################################################


class Game:

    # PRIVATE:
    def __init__(self, bomb_count, grid_size_x, grid_size_y):

        # Class initialisation
        self.__gameOver = False
        self.__bombs = bomb_count  # storing total amount of bombs for future reference
        self.__sizeX = grid_size_x  # storing the grid size for future reference and optimisation
        self.__sizeY = grid_size_y  # storing the grid size for future reference and optimisation

        # 2D object array of type tile that represents the game board
        self.__gameArray = np.ndarray((self.__sizeX, self.__sizeY), dtype=np.object)
        for x in range(self.__sizeX):
            for y in range(self.__sizeY):
                self.__gameArray[x, y] = Tile()

        # 2D int array to count the amount of bombs within one tile of current index, 9 represents the bombs location
        self.__guideArray = np.zeros((self.__sizeX, self.__sizeY), dtype=int)

    # Function that creates the guide array with only the bomb locations
    def __field_generate(self, first_move_x, first_move_y):  # generates the desired amount of bombs in the desired size field

        bomb_count = 0  # used to make sure that the right amount of bombs have been placed
        chance = self.__sizeX*self.__sizeY  # makes the chance of a bomb on that tile fair with all tiles
        while bomb_count < self.__bombs:
            for x in range(0, self.__sizeX):
                for y in range(0, self.__sizeY):
                    if self.__guideArray[x, y] != 9 and bomb_count >= self.__bombs and random.randint(0, chance - (bomb_count + 1)) == 0 and x != first_move_x and y != first_move_y:
                        self.__guideArray[x, y] = 9
                        bomb_count += 1

    # Function that updates the guide array with the bomb adjacency
    def __guide_create(self):  # looks at each point in the field and sees how many bombs are adjacent to the index
        for x in range(0, self.__sizeX):
            for y in range(0, self.__sizeY):
                for i in range(x-1, x+2):
                    for j in range(y-1, y+2):
                        if i in range(0, self.__sizeX) and j in range(0, self.__sizeY) and self.__guideArray[x, y] != 9:
                            if self.__guideArray[i, j] == 9:
                                self.__guideArray[x, y] += 1

    # Function that draws the game array from the guide array
    def __solution_draw(self):  # combines the guide with the mine map to create the mapped solution
        for x in range(0, self.__sizeX):
            for y in range(0, self.__sizeY):
                self.__gameArray[x, y].generate(self.__guideArray[x, y])

    # PUBLIC:
    def new_board(self, x, y):  # sets up a new board. NOTICE: this doesn't necessarily reset the board
        self.__field_generate(x, y)
        self.__guide_create()
        self.__solution_draw()
        self.__gameOver = False  # used to show that the game has started

    # function that resets boards to default values allows for some settings like bomb_count and size to be preserved
    def reset_board(self):
        for x in range(0, self.__sizeX):
            for y in range(0, self.__sizeY):
                self.__guideArray[x, y] = 0
                self.__gameArray[x, y].generate(0)

    def mine_test(self, x, y):  # returns if there is a mine at said location
        if self.__guideArray[x, y] == 9:
            return True
        else:
            return False

    def debug_show_solution(self):  # returns the specified tile in the solution
        output = np.zeros((self.__sizeX, self.__sizeY), dtype=int)
        for x in range(0, self.__sizeX):
            for y in range(0, self.__sizeY):
                output[x, y] = self.__gameArray[x, y].debug_get_tile_type()
        return output

    def debug_lc(self, x, y):
        self.__gameOver = self.__gameArray[x, y].left_click()
        return self.__gameOver

    def get_game_over(self):
        return self.__gameOver
# END OF GAME CLASS ####################################################################################################


class Window:

    def __init__(self):
        self.width = 9
        self.height = 9
        self.bombs = 10
        self.tile_size = 16

        app = QtWidgets.QApplication(sys.argv)
        game_window = QtWidgets.QWidget()
        game_window.setWindowTitle("MultiSweeper V0.1")
        game_window.resize(self.tile_size*(self.width+2), self.tile_size*(self.height+2))
        # game_window.show()
        self.new_game()
        sys.exit(app.exec_())

    # def draw(self):

    def new_game(self):
        app = QtWidgets.QApplication(sys.argv)

        new_game_diag = QDialog()
        new_game_diag.setWindowTitle("New Game")
        new_game_diag.resize(100, 100)
        new_game_diag.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)

        lbl_bombcount = QtWidgets.QLabel("Bombs:", new_game_diag)
        lbl_bombcount.move(10, 10)
        txt_bombcount = QLineEdit("10", new_game_diag)
        txt_bombcount.move(50, 10)
        txt_bombcount.resize(40, 20)

        lbl_width = QtWidgets.QLabel("Width:", new_game_diag)
        lbl_width.move(10, 30)
        txt_width = QLineEdit("9", new_game_diag)
        txt_width.move(50, 30)
        txt_width.resize(40, 20)

        lbl_height = QtWidgets.QLabel("Height:", new_game_diag)
        lbl_height.move(10, 50)
        txt_height = QLineEdit("9", new_game_diag)
        txt_height.move(50, 50)
        txt_height.resize(40, 20)

        btn_generate = QPushButton(new_game_diag)
        btn_generate.setText("Generate!")
        btn_generate.move(10, 70)
        btn_generate.clicked.connect(self.generate(int(txt_width.text()), int(txt_height.text()), int(txt_bombcount.text())))
        #btn_generate.pressed.connect(self.generate(int(txt_width.text()), int(txt_height.text()), int(txt_bombcount.text())))

        new_game_diag.show()

        sys.exit(app.exec_())

    def generate(self, x, y, b):
        self.width = x
        self.height = y
        self.bombs = b

# END OF WINDOW CLASS ##################################################################################################


app = QtWidgets.QApplication(sys.argv)
Window()
sys.exit(app.exec_())
