import numpy as np
import random


class Game:

    # PRIVATE:
    def __init__(self, bomb_count, grid_size):
        self.__bombs = bomb_count  # storing total amount of bombs for future reference
        self.__size = grid_size  # storing the grid size for future reference and optimisation

        self.__mineArray = np.zeros((self.__size, self.__size), dtype=bool)
        # ^ stores a boolean array for bombs for referencing, tests and optimization
        self.__gameArray = np.zeros((self.__size, self.__size), dtype=str)
        # ^ stores a string array to act as a temporary solution board
        self.__guideArray = np.zeros((self.__size, self.__size), dtype=int)
        # ^ stores a int array to count the amount of bombs within one tile of current index

        self.new_board()  # stores a boolean array for bombs for referencing, tests and optimization

    # generate
    # \/
    def __field_generate(self):  # generates the desired amount of bombs in the desired size field
        bomb_count = 0
        iterations = 0
        chance = self.__size*self.__size
        while bomb_count < self.__bombs:
            implement = False
            for x in range(0, self.__size):
                for y in range(0, self.__size):
                    if not self.__mineArray[x, y] and not implement and random.randint(0, chance) == 0:
                        self.__mineArray[x, y] = True
                        bomb_count += 1
                        iterations += 1
                        implement = True

    # \/

    def __guide_create(self):  # looks at each point in the field and sees how many bombs are adjacent to the index
        for x in range(0, self.__size):
            for y in range(0, self.__size):
                for i in range(x-1, x+2):
                    for j in range(y-1, y+2):
                        if 0 <= i < self.__size and 0 <= j < self.__size:
                            if self.__mineArray[i, j]:
                                self.__guideArray[x, y] += 1
                        elif self.__mineArray[x, y]:
                            self.__guideArray[x, y] = 9

    # \/

    def __solution_draw(self):  # combines the guide with the mine map to create the mapped solution
        for x in range(0, self.__size):
            for y in range(0, self.__size):
                if self.__mineArray[x, y]:
                    self.__gameArray[x, y] = "+"
                elif self.get_solution_index(x, y) == 0:
                    self.__gameArray[x, y] = " "
                else:
                    self.__gameArray[x, y] = chr(self.__guideArray[x, y] + 48)

    # PUBLIC:
    def new_board(self):  # sets up a new board, notice, this doesn't necessarily reset the board
        self.__field_generate()
        self.__guide_create()
        self.__solution_draw()

    # function that resets boards to default values allows for some settings like bomb_count and size to be preserved
    def reset_board(self):
        for x in range(0, self.__size):
            for y in range(0, self.__size):
                self.__mineArray[x, y] = False
                self.__guideArray[x, y] = 0
                self.__gameArray[x, y] = " "

    def mine_test(self, x, y):  # returns if there is a mine at said location
        return self.__mineArray[x, y]

    def get_solution_index(self, x, y):  # returns the specified tile in the solution
        return self.__gameArray[x, y]

    def get_solution(self):  # returns the whole solution
        return self.__gameArray

    def get_size(self):  # returns the size of the field
        return self.__size


class Tile:

    # Class initialisation
    def __init__(self, value, x, y):
        self.x_pos = x  # stores x value of tile << May not need
        self.y_pos = y  # stores y value of tile << May not need
        self.tile_type = value  # stores the type of tile, 0-8 = bomb adjacency, 9 = bomb

        self.flagged = False  # stores if the tile has been flagged
        self.clicked = False  # stores if the tile has been clicked

        # stores the image of the tile
        # self.tile_img = QtWidgets.QLabel()
        # self.tile_img.setPixmap(QtGui.QPixmap("unknown.png"))

        # stores if the tile is a bomb or not
        self.bomb = False
        if self.tile_type == 9:
            self.bomb = True

        self.PLACEHOLDER = None

    # function for what to do when the tile is left clicked
    def left_click(self):
        if not self.flagged and not self.clicked:  # makes sure that the tile has not been flagged
            self.clicked = True  # saves processing time
            if 0 <= self.tile_type < 9:  # if the tile is an adjacency tile
                self.PLACEHOLDER
                # self.tile_img.setPixmap(QtGui.QPixmap(str(self.tile_type)+".png"))

            elif self.tile_type == 9:  # if the tile is a bomb
                self.PLACEHOLDER
                # self.tile_img.setPixmap(QtGui.QPixmap("bomb.png"))

            else:
                print("ERROR: [" + self.x_pos + "," + self.y_pos + "]s' tile_type value is out of range.")  # DEBUG
            return self.bomb
        return False

    # function for what to do when the tile is right clicked
    def right_click(self):
        if not self.clicked:  # makes sure that the tile has not already been clicked
            if self.flagged:
                # self.tile_img.setPixmap(QtGui.QPixmap("unknown.png"))
                self.flagged = False
            else:
                # self.tile_img.setPixmap(QtGui.QPixmap("flag.png"))
                self.flagged = True
        return self.flagged