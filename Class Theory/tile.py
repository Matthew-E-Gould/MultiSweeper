from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QGridLayout, QHBoxLayout


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
