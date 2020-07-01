# This class contains all functionality relating to the user
import mysql.connector
import bcrypt

class User():

    def __init__(self, username, password):
        global cnx
        cnx = mysql.connector.connect(user='team', password='', host='ccargill.com', database='ms_main')
        self.user_login()

    # BEGIN register a new user account---
    def register(username, password, email):
        cursor = cnx.cursor()  # Create new database connection
        cursor.execute(
            "INSERT INTO users(us_name, us_email, us_pass) VALUES (%s, %s, %s)",
            (username, email, password))
        cnx.commit()  # Commit update to database
        cursor.close()
    # END register a new user account---

    #BEGIN user login---
    def user_login(username, password):
        # Fetch the users password to check against
        cursor = cnx.cursor()
        # Select the activated status of the user account record
        cursor.execute("SELECT us_pass FROM users WHERE us_name= %s", (username,))
        for (us_pass) in cursor:
            returned_pass = us_pass
            converted_pass = ''.join(map(str, returned_pass))  # Convert tuple result to string

        # Check password entered is same as the stored one
        passwords_match = bcrypt.checkpw(password, converted_pass)
        if passwords_match:
            login_success = 1
        else:
            login_success = 0

        # Close database connection
        cursor.close()
        return login_success
        # END user login---

