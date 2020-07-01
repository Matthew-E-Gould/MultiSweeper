# This file contains all the functionality related to uploading, downloading and creating games with the database.
import mysql.connector

class Database_Logic():
    # Contains all database function
    global cnx
    # Define database connection settings
    cnx = mysql.connector.connect(user='minesweeper', password='', host='ccargill.com', database='minesweeper')

    # Upload a new game grid into the database into a new table
    def upload_new_game(self, game_id, game_array, width, height):
        cursor = cnx.cursor()  # Create database connection
        # Create new table with unique name and setup columns as needed to store a move:
        # 1- id of the tile in the database
        # 2- value of the tile (bomb , 1, 2, 3)
        # 3- who revealed the tile
        # 4- if the tile has been revealed or not
        cursor.execute("CREATE TABLE %s (mov_id MEDIUMINT NOT NULL AUTO_INCREMENT, mov_value VARCHAR(255), mov_turn INT, revealed INT)")

        # For each of the x,y positions in the array, create a new record in the table
        for y in range(0, height):
            for x in range(0, width):
                cursor.execute("INSERT INTO %s (%s,%s)",(game_array.))