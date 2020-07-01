import numpy as np
import random
from tkinter import *
import time


class Tile:

    def __init__(self):

        # Class initialisation
        self.tile_type = 0  # stores the type of tile, 0-8 = bomb adjacency, 9 = bomb
        self.flagged = False  # stores if the tile has been flagged
        self.clicked = False  # stores if the tile has been clicked
        self.bomb = False  # stores if the tile is a bomb or not

    def generate(self, value):
        self.tile_type = value  # stores the type of tile, 0-8 = bomb adjacency, 9 = bomb
        if 0 <= self.tile_type < 9:
            self.bomb = False
        elif self.tile_type == 9:
            self.bomb = True
        else:
            print("ERROR: tile_type value (" + str(self.tile_type) + ") is outside of range [0-9].")  # DEBUG

    # function for what to do when the tile is left clicked
    def left_click(self):
        if not self.flagged and not self.clicked:  # makes sure that the tile has not been flagged
            self.clicked = True  # sets that the tile was clicked
            return self.tile_type
        return False

    # function for what to do when the tile is right clicked
    def right_click(self):
        if not self.clicked:  # makes sure that the tile has not already been clicked
            if self.flagged:
                self.flagged = False
            else:
                self.flagged = True
        return self.flagged

    def get_clicked(self):
        return self.clicked

    def get_flagged(self):
        return self.flagged

########################################################################################################################
# END OF TILE CLASS ####################################################################################################
########################################################################################################################


class Game:

    # PRIVATE:
    def __init__(self, grid_size_x, grid_size_y, bomb_count):
        # Class initialisation
        self.gameOver = False
        self.sizeX = grid_size_x  # storing the grid size for future reference and optimisation
        self.sizeY = grid_size_y  # storing the grid size for future reference and optimisation
        self.bombs = bomb_count  # storing total amount of bombs for future reference
        # 2D object array of type tile that represents the game board
        self.gameArray = np.ndarray((self.sizeX, self.sizeY), dtype=np.object)
        for x in range(self.sizeX):
            for y in range(self.sizeY):
                self.gameArray[x, y] = Tile()
        # 2D int array to count the amount of bombs within one tile of current index, 9 represents the bombs location
        self.guideArray = np.zeros((self.sizeX, self.sizeY), dtype=int)

    # Function that creates the guide array with only the bomb locations
    def __field_generate(self, first_move_x, first_move_y):  # generates a set amount of bombs in the desired size field
        # initialisation
        selection = []
        x_vec = []
        y_vec = []
        # creating a list for selection values
        for x in range(0, self.sizeX):
            for y in range(0, self.sizeY):
                selection.append([x, y])
        # removing the first moves index
        selection.remove([first_move_x, first_move_y])
        # while the amount of generated values is less than desired bomb amount
        while len(x_vec) < self.bombs:
            # selects and removes a value from the list
            value = random.choice(selection)
            selection.remove(value)
            # gets the XY co-ord and adds it to the correct vector
            x_vec.append(value[0])
            y_vec.append(value[1])
        # clears the list since it's not needed anymore
        selection.clear()
        # adds the selected locations as bombs
        for x in range(0, self.bombs):
            self.guideArray[x_vec[x], y_vec[x]] = 9

    # Function that updates the guide array with the bomb adjacency
    def __guide_create(self):  # looks at each point in the field and sees how many bombs are adjacent to the index
        for x in range(0, self.sizeX):
            for y in range(0, self.sizeY):
                for i in range(x-1, x+2):
                    for j in range(y-1, y+2):
                        if i in range(0, self.sizeX) and j in range(0, self.sizeY) and self.guideArray[x, y] != 9:
                            if self.guideArray[i, j] == 9:
                                self.guideArray[x, y] += 1

    # Function that draws the game array from the guide array
    def __solution_draw(self):  # combines the guide with the mine map to create the mapped solution
        for x in range(0, self.sizeX):
            for y in range(0, self.sizeY):
                self.gameArray[x, y].generate(self.guideArray[x, y])

    # PUBLIC:
    def new_board(self, x_size, y_size):  # sets up a new board
        self.__field_generate(x_size, y_size)
        self.__guide_create()
        self.__solution_draw()

    def is_clear(self, x, y):  # returns if there is a mine at said location
        if self.guideArray[x, y] == 0:
            return True
        else:
            return False

    def left_click(self, x, y):  # runs the left click function in the __gameArray class
        temp_int = self.gameArray[x, y].left_click()
        if temp_int == 9:
            self.__gameOver = True
        return temp_int

    def right_click(self, x, y):  # runs the right click function in the __gameArray class
        flagged = self.gameArray[x, y].right_click()
        return flagged

    def get_game_over(self):  # returns if the game is over
        return self.__gameOver

    def get_clicked(self, x, y):  # returns if the tile has been clicked
        temp_bool = self.gameArray[x, y].get_clicked()
        return temp_bool

    def get_flagged(self, x, y):  # returns if the tile has been flagged
        temp_bool = self.gameArray[x, y].get_flagged()
        return temp_bool

    def get_grid(self):
        return self.gameArray

########################################################################################################################
# END OF GAME CLASS ####################################################################################################
########################################################################################################################


class Asset:

    def __init__(self):  # initialisation function
        self.directory = "ASSETS/"

        self.unknown = "unknown.png"
        self.flag = "flag.png"
        self.bomb = "bomb.png"

        self.number = ["0.png", "1.png", "2.png", "3.png", "4.png", "5.png", "6.png", "7.png", "8.png"]

    def change_directory(self, location):
        self.directory = location

    def asset(self, val):
        if isinstance(val, int):
            index = int(val)
            if 0 >= index > 9:
                output = self.directory + self.number[index]
            else:
                print("ERROR: val value (" + str(val) + ") is outside of range [0-8].")
                output = "error"
        else:
            if val == "F" or val == "f" or val == "Flag" or val == "flag":
                output = self.directory + self.flag
            elif val == "B" or val == "b" or val == "Bomb" or val == "bomb":
                output = self.directory + self.flag
            elif val == "U" or val == "u" or val == "Unknown" or val == "unknown":
                output = self.directory + self.unknown
            else:
                print("ERROR: val value ("+val+") is not a valid input.")
                output = "error"

        return output

########################################################################################################################
# END OF ASSETS CLASS ##################################################################################################
########################################################################################################################


class Window:

    def __init__(self):  # initialisation function
        # general initialisation
        self.start_time = time.time()
        self.end_time = time.time()
        self.button_list = []
        self.width = self.height = 9
        self.bombs_left = self.bombs = 10
        self.tiles_left = self.width * self.height
        self.tile_size = 16
        self.game = Game(self.width, self.height, self.bombs)
        self.first_move = True
        self.finished = False

        # initialising window
        self.root = Tk()
        self.root.title("MultiSweeper 20/07/2018 build")

        # creating window frames for games and options
        ui_frame = Frame()
        ui_frame.grid(row=0)

        stats_frame = Frame()
        stats_frame.grid(row=1)

        self.game_frame = Frame()
        self.game_frame.grid(row=2)

        feedback_frame = Frame()
        feedback_frame.grid(row=3)

        # creating text to give feedback if the user is playing, has (won/lost) or even is connecting
        self.lbl_feedback = Label(feedback_frame)
        self.lbl_feedback.pack()

        # creating and drawing buttons on the window
        btn_reset = Button(ui_frame, text="Reset Board", command=lambda: self.new_game())
        btn_reset.grid(row=0, column=0)
        btn_newgame = Button(ui_frame, text="New Game", command=lambda: self.new_game_input(False))
        btn_newgame.grid(row=0, column=1)

        # creating and drawing bomb's left text
        self.lbl_bombs_left = Label(stats_frame, text="Bombs Left: "+str(self.bombs_left))
        self.lbl_bombs_left.grid(row=0, column=0)
        self.lbl_tiles_left = Label(stats_frame, text="Tiles Left: " + str(self.tiles_left))
        self.lbl_tiles_left.grid(row=0, column=1)

        # starting game
        self.new_game()

        # keeping window alive
        self.root.mainloop()

    def new_game_input(self, error):  # Function that creates a window for the user to change the board size
        # initialising new game window
        win_newgame = Tk()
        win_newgame.title("New Game")
        win_newgame.resizable(width=FALSE, height=FALSE)
        # setting what text should appear at the top of the window
        if error:
            lbl_context = Label(win_newgame, text="An error had occurred. Please make sure you only enter numbers.",
                                fg="red")
        else:
            lbl_context = Label(win_newgame, text="Input values for a new game of MultiSweeper.", fg="black")

        # initialising textbox's text part 1
        bomb_text = StringVar(win_newgame)
        height_text = StringVar(win_newgame)
        width_text = StringVar(win_newgame)
        bomb_text.set(self.bombs)
        width_text.set(self.width)
        height_text.set(self.height)

        lbl_context.grid(row=0, columnspan=3)

        # setting up other texts, drawing them to specified locations and aligning them to the east of their space
        lbl_bombcount = Label(win_newgame, text="Bombs:")
        lbl_bombcount.grid(row=1, sticky=E)

        lbl_width = Label(win_newgame, text="Width:")
        lbl_width.grid(row=2, sticky=E)

        lbl_height = Label(win_newgame, text="Height:")
        lbl_height.grid(row=3, sticky=E)

        # setting up input boxes and drawing them to specified locations
        txt_bombcount = Entry(win_newgame, textvariable=bomb_text, width=6)
        txt_bombcount.grid(row=1, column=1)

        txt_width = Entry(win_newgame, textvariable=width_text, width=6)
        txt_width.grid(row=2, column=1)

        txt_height = Entry(win_newgame, textvariable=height_text, width=6)
        txt_height.grid(row=3, column=1)

        # setting up the generate button and drawing it to specified location (also programming buttons click function)
        btn_generate = Button(win_newgame, text="Generate!",
                              command=lambda: (self.generate(txt_width.get(), txt_height.get(), txt_bombcount.get()),
                                               win_newgame.destroy()))
        btn_generate.grid(row=4, columnspan=3)

        # easy, medium & hard buttons
        btn_easy = Button(win_newgame, text="Easy", width=6, command=lambda: (bomb_text.set(10),
                                                                              width_text.set(9),
                                                                              height_text.set(9)))
        btn_easy.grid(row=1, column=2)
        btn_medium = Button(win_newgame, text="Medium", width=6, command=lambda: (bomb_text.set(40),
                                                                                  width_text.set(15),
                                                                                  height_text.set(13)))
        btn_medium.grid(row=2, column=2)
        btn_hard = Button(win_newgame, text="Hard", width=6, command=lambda: (bomb_text.set(99),
                                                                              width_text.set(30),
                                                                              height_text.set(16)))
        btn_hard.grid(row=3, column=2)

    def generate(self, x, y, b):
        # input validation used as an effective if statement
        try:
            self.width = int(x)
            self.height = int(y)
            # input validation
            if int(b) >= int(x)*int(y):
                self.bombs = int(x)*int(y)-1
            else:
                self.bombs = int(b)
            # runs the new game function
            self.new_game()
        except ValueError:
            # re-opens new game window since outputs were incorrect, new game window will show error text
            self.new_game_input(True)

    def new_game(self):
        # initialising the game to correct settings
        self.finished = False
        self.first_move = True
        self.button_list = []
        self.game = Game(self.width, self.height, self.bombs)
        self.bombs_left = self.bombs
        self.tiles_left = self.width * self.height

        # updating the stats field
        self.update_stats(0, 0)

        # updating the game field
        self.game_frame.destroy()
        self.game_frame = Frame()
        self.game_frame.grid(row=2)

        # updating the feedback field
        self.lbl_feedback.config(text="Play!", fg="black")

        self.build()

    def auto_reveal(self, x_input, y_input):  # function that reveals all the tiles needed when a clear tile is clicked
        # initialisation
        val = 0
        vec_x = []
        vec_y = []
        # appending inputs to vectors so while loop will run
        vec_x.append(x_input)
        vec_y.append(y_input)
        # when we've gone through the entire vector end while loop
        while (len(vec_x) - val) > 0:
            # registering tile as save to reveal information from it
            self.left_click(vec_x[val], vec_y[val], True, True)
            # if the current tile is clear then move on
            if self.game.is_clear(vec_x[val], vec_y[val]):
                # getting surrounding tiles
                for x in range(vec_x[val]-1, vec_x[val]+2):
                    for y in range(vec_y[val]-1, vec_y[val]+2):
                        # if the tile already appears in the vectors then don't add it again
                        # (needed to avoid infinite loop)
                        failed = False
                        if 0 <= x < self.width and 0 <= y < self.height:
                            for z in range(0, len(vec_x)):
                                if x == vec_x[z] and y == vec_y[z]:
                                    failed = True
                        else:
                            failed = True
                        # adding values to vector if they are valid
                        if not failed:
                            vec_x.append(x)
                            vec_y.append(y)
            # counting how many times program has gone trough the loop
            val += 1

    def build(self):  # function that draws all the buttons to the game_frame
        count = 0
        for y in range(0, self.height):
            for x in range(0, self.width):
                self.button_list.append(Button(self.game_frame, text="?", height=1, width=1, bg="black", fg="white"))
                self.button_list[count].bind("<Button-1>", lambda event, i=x, j=y: self.left_click(i, j, False, False))
                self.button_list[count].bind("<Button-3>", lambda event, i=x, j=y: self.right_click(i, j))
                self.button_list[count].grid(column=x, row=y)
                count += 1

    def left_click(self, x, y, auto_reveal, second_click):  # function for when the button is left clicked
        # initialisation
        clear = False
        bomb = 0
        # equation that works out the index for the selected tiles X,Y pos
        index = x + (y * self.width)
        # if the tile hasn't been clicked yet run the reveal functionality, also makes sure the tile isn't flagged
        if not self.game.get_flagged(x, y) and not self.game.get_clicked(x, y) and not self.game.get_game_over():
            # generates the field if it is the first move
            if self.first_move:
                self.first_move = False
                self.game.new_board(x, y)
                self.start_time = time.time()
            # clicks the tile
            tile_value = self.game.left_click(x, y)
            # works out what to display based off of what the tiles value is and reduces the bomb count if necessary
            if tile_value == 0:
                self.button_list[index].config(text=" ", bg="green")
                clear = True
            elif tile_value == 9:
                self.button_list[index].config(text="*", fg="black", bg="red")
                bomb -= 1
            else:
                self.button_list[index].config(text=str(tile_value), fg="green", bg="white")
            # if the parent function isn't the auto reveal function (used to reduce data spam)
            if not auto_reveal:
                self.send_move(x, y, True)
                # if the tile was a clear tile then run the auto reveal function
                if clear:
                    # start = time.time()
                    self.auto_reveal(x, y)
                    # end = time.time()
                    # total = end - start
                    # print("function 'auto_reveal' completed in", str(round(total, 3))+"s")
            # updates the tile count and updates the UI relating to the values
            self.update_stats(bomb, -1)
            # loss condition
            if self.game.get_game_over():
                self.end(False)
            # win condition
            elif self.tiles_left == self.bombs_left == 0:  # use of first == instead of 'and'
                self.end(True)
        # statement that reveals surrounding tiles if suitable amount of tiles have been flagged
        elif self.game.get_clicked(x, y) and not second_click:
            # getting the buttons text
            tile_value = self.button_list[index]["text"]
            # input validation
            if not tile_value == "F" and not tile_value == "*" and not tile_value == " ":
                # checking how many surrounding tile are flagged
                for x_index in range(x-1, x+2):
                    for y_index in range(y-1, y+2):
                        if 0 <= x_index < self.width and 0 <= y_index < self.height \
                                and self.game.get_flagged(x_index, y_index):
                            bomb += 1
                # checking that enough surrounding tiles are flagged
                if bomb == int(tile_value):
                    # revealing surrounding tiles
                    for x_index in range(x - 1, x + 2):
                        for y_index in range(y - 1, y + 2):
                            if 0 <= x_index < self.width and 0 <= y_index < self.height:
                                self.left_click(x_index, y_index, False, True)

    def right_click(self, x, y):  # function for when the button is right clicked
        # equation that works out the index for the selected tiles X,Y pos
        index = x+(y*self.width)
        # makes sure that the user doesnt try to RC the tile when game is over
        if not self.finished:
            # makes sure that it's not the first move since first tile can't be bomb
            if not self.first_move and not self.game.get_game_over():
                # makes sure that the tile isn't flagged.
                if not self.game.get_clicked(x, y):
                    # decides what to do based off of if the tile is already flagged or not
                    if self.game.right_click(x, y):
                        self.button_list[index].config(text="F", fg="red", bg="white")
                        self.update_stats(-1, -1)
                    else:
                        self.button_list[index].config(text="?", fg="white", bg="black")
                        self.update_stats(1, 1)
                    # updates the UI for the stats since they have changed

                    self.send_move(x, y, False)
                # win condition
                if self.tiles_left == self.bombs_left == 0:
                    self.end(True)

    def update_stats(self, bombs, tiles):  # function for updating the stats in the UI

        self.bombs_left += bombs
        self.tiles_left += tiles

        bomb_colour = "red"  # indicates that too many flags are on the field
        tile_colour = "red"  # shouldn't be possible but kept for debugging and clarity

        # colour coding based off of value
        if self.bombs_left > 0:
            bomb_colour = "black"
        elif self.bombs_left == 0:
            bomb_colour = "green"

        if self.tiles_left > 0:
            tile_colour = "black"
        elif self.tiles_left == 0:
            tile_colour = "green"

        # updates the actual labels
        self.lbl_bombs_left.configure(text="Bombs Left: " + str(self.bombs_left), fg=bomb_colour)
        self.lbl_tiles_left.configure(text="Tiles Left: " + str(self.tiles_left), fg=tile_colour)

    def end(self, win):  # end function for the game, updates the feedback field
        self.end_time = time.time()
        score = self.end_time - self.start_time
        score = round(score, 3)
        total_time = str(score)+"s"
        self.finished = True

        if win:
            self.lbl_feedback.config(text="Completed in "+total_time, fg="green")
        else:
            self.lbl_feedback.config(text="Lost in "+total_time, fg="red")
            # disables buttons when game is lost
            for x in range(0, len(self.button_list)):
                self.button_list[x].config(state="disabled")

    def send_move(self, x, y, left):  # send move function, does nothing useful yet (SUGGESTION FOR CONNOR)
        # x is x location of click
        # y is y location of click
        # left is a bool (as an int) allowing receiver/server is receiving a left click or not
        # could use a CSV format where the whole thing is passed as a string, for example:
        if left:
            output = "1,"
        else:
            output = "0,"
        output = output+str(x)+","+str(y)

        print("SENT:", output)  # [left/right]click, x position, y position
        # with this setup 2 in the fist field could be used to indicate new game
        # for receiving you can use the [right/left]_click commands since they update the button anyway

    def get_game_grid(self):
        return self.game.get_grid()


########################################################################################################################
# END OF WINDOW CLASS ##################################################################################################
########################################################################################################################

Window()  # runs the program, duh.
