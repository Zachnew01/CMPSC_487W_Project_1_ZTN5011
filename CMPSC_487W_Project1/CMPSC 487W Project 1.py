# -------------------------------------------
#
# CMPSC 487W - Project 1 - Sun Lab Access System
#
# Zachary T. Newman
#
# -------------------------------------------

import mysql.connector
from mysql.connector import errorcode
import datetime

import sys
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtCore import QDate, QTime, QDateTime, Qt
from LoginScreen import Ui_loginscreen
from AdminScreen import Ui_adminscreen

loginSuccess = False
try: # Connect to the database globally so all functions can access crsr
    mydb = mysql.connector.connect(
        host="localhost",
        user="admin",
        password="ztn5011SQL",
        database="sunlabaccesssystem"
    )
    print("Connected to Database\n")
    crsr = mydb.cursor()
except mysql.connector.Error as err:
    print(err)
# END OF GLOBAL MYSQL CONNECTION


class LoginScreen(QtWidgets.QMainWindow, Ui_loginscreen): # Class for Login Screen/Menu
    def __init__(self, *args, obj=None, **kwargs):
        super(LoginScreen, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # Allows for the buttons to work correctly by calling the associated function
        self.loginButton.clicked.connect(self.loginFunc)
        self.passwordField.setEchoMode(QLineEdit.EchoMode.Password)
    # END OF __init__

    def loginFunc(self):
        username = self.usernameField.text()
        password = self.passwordField.text()
        if(username == "Admin" and password == "pwSQL"):
            self.outputLabel.setText("Login Successful")
            global loginSuccess
            loginSuccess = True
            self.close()
        else:
            self.outputLabel.setText("Username or Password Invalid")
    # END OF loginFunc

# END OF LoginScreen


class AdminScreen(QtWidgets.QMainWindow, Ui_adminscreen): # Class for Login Screen/Menu
    def __init__(self, *args, obj=None, **kwargs):
        super(AdminScreen, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.resize(700, 361)
        # Ensure inputs into the id input fields are 9-digit numbers
        self.SLA_id_field.setInputMask('999999999')
        self.SU_id_field.setInputMask('999999999')

        # Allows for the buttons to work correctly by calling the associated function
        self.SLA_search_button.clicked.connect(self.search)
        self.searchDuring.clicked.connect(self.search_During)
        self.searchBetween.clicked.connect(self.search_Between)

        self.activateUser.clicked.connect(self.activate_User)
        self.suspendUser.clicked.connect(self.suspend_User)

        global crsr
        try: # initialize the tables for the Sun Lab Accesses and the System Users to all entries
            crsr.execute("SELECT * FROM accesses")
            result = crsr.fetchall()
            self.SLA_result_field.insertPlainText("  User ID  |      Date Time      | isValid \n")
            for x in result:
                userID = x[0]
                dateTime = str(x[1])
                isValid = str(x[2])
                self.SLA_result_field.insertPlainText(" " + userID + " | " + dateTime + " | " + isValid + "\n")

            crsr.execute("SELECT * FROM sysusers")
            result = crsr.fetchall()
            self.SU_result_field.insertPlainText("  User ID  |      User Type       | isActive \n")
            for x in result:
                userID = x[0]
                userType = '{:20s}'.format(x[1])
                isActive = str(x[2])
                self.SU_result_field.insertPlainText(" " + userID + " | " + userType + " | " + isActive + "\n")
        except mysql.connector.Error as err:
            print(err)
    # END OF __init__

    # SLA_result_field - query results for table 'accesses'
    # SU_result_field - query results for table 'sysusers'

    def search(self):
        global crsr
        inputID = self.SLA_id_field.text()
        try:
            if (inputID == ""): # Resets the Sun Lab Accesses table when no user ID is given
                self.SLA_Feedback.setText("Displaying all accesses")
                crsr.execute("SELECT * FROM accesses")
                result = crsr.fetchall()
                self.SLA_result_field.clear()
                self.SLA_result_field.insertPlainText("  User ID  |      Date Time      | isValid \n")
                for x in result:
                    userID = x[0]
                    dateTime = str(x[1])
                    isValid = str(x[2])
                    self.SLA_result_field.insertPlainText(" " + userID + " | " + dateTime + " | " + isValid + "\n")
            else: # Only Displays access attempts from the specified user ID
                self.SLA_Feedback.setText("Displaying accesses by user " + inputID)
                sql = "SELECT * FROM accesses WHERE aID = %s"
                sqlInput = (inputID,)
                crsr.execute(sql, sqlInput)
                result = crsr.fetchall()
                self.SLA_result_field.clear()
                self.SLA_result_field.insertPlainText("  User ID  |      Date Time      | isValid \n")
                for x in result:
                    userID = x[0]
                    dateTime = str(x[1])
                    isValid = str(x[2])
                    self.SLA_result_field.insertPlainText(" " + userID + " | " + dateTime + " | " + isValid + "\n")
        except mysql.connector.Error as err:
            print(err)    
    # END OF search

    def search_During(self):
        # select * from accesses where Date(aTime) like 'inputDate'
        global crsr
        inputDate = self.startTime.date()
        inputDate = inputDate.toString(Qt.DateFormat.ISODate)
        try:
            self.SLA_Feedback.setText("Displaying all accesses on " + str(inputDate))
            
            sql = "SELECT * FROM accesses WHERE Date(aTime) like %s"
            sqlInput = (inputDate,)
            crsr.execute(sql, sqlInput)
            result = crsr.fetchall()
            self.SLA_result_field.clear()
            self.SLA_result_field.insertPlainText("  User ID  |      Date Time      | isValid \n")
            for x in result:
                userID = x[0]
                dateTime = str(x[1])
                isValid = str(x[2])
                self.SLA_result_field.insertPlainText(" " + userID + " | " + dateTime + " | " + isValid + "\n")
        except mysql.connector.Error as err:
            print(err)
    # END OF search_During

    def search_Between(self):
        # select * from accesses where aTime between 'startDate' and 'endDate';
        global crsr
        inputStartDate = self.startTime.dateTime()
        inputEndDate = self.endTime.dateTime()
        inputStartDate = inputStartDate.toString(Qt.DateFormat.ISODate)
        inputEndDate = inputEndDate.toString(Qt.DateFormat.ISODate)
        inputStartDate = inputStartDate[0:10] + " " + inputStartDate[11:]
        inputEndDate = inputEndDate[0:10] + " " + inputEndDate[11:]
        try:
            if(inputStartDate < inputEndDate): # Check to see if the time range makes sense, otherwise display error
                self.SLA_Feedback.setText("Accesses between " + str(inputStartDate) + " & " + str(inputEndDate))
                sql = "SELECT * FROM accesses WHERE aTime BETWEEN %s AND %s"
                sqlInput = (inputStartDate,inputEndDate)
                crsr.execute(sql, sqlInput)
                result = crsr.fetchall()
                self.SLA_result_field.clear()
                self.SLA_result_field.insertPlainText("  User ID  |      Date Time      | isValid \n")
                for x in result:
                    userID = x[0]
                    dateTime = str(x[1])
                    isValid = str(x[2])
                    self.SLA_result_field.insertPlainText(" " + userID + " | " + dateTime + " | " + isValid + "\n")
            else:
                self.SLA_Feedback.setText("Error - Invalid Time Range")
        except mysql.connector.Error as err:
            print(err)
    # END OF search_Between

    def activate_User(self): # Adds user ID to sysusers if they aren't already activated, or reactivates them if they are already in sysusers
        global crsr
        inputID = self.SU_id_field.text()
        inputType = self.SU_type_field.text()
        try:
            if(inputID == ""):
                self.SU_Feedback.setText("Error - Incomplete Input")
            else:
                sql = "SELECT * FROM sysusers WHERE id = %s"
                sqlInput = (inputID,)
                crsr.execute(sql, sqlInput)
                result = crsr.fetchall()
                if((not result) and (inputType == "" or len(inputType) >= 20)):
                    self.SU_Feedback.setText("Error - Incomplete Input")
                else:
                    if(result):
                        self.SU_Feedback.setText("Reactivating user " + inputID)
                        sql = "UPDATE sysusers SET isActive = 1 WHERE id = %s"
                        sqlInput = (inputID,)
                        crsr.execute(sql, sqlInput)
                        crsr.execute("Commit")
                    else:
                        self.SU_Feedback.setText("Activating user " + inputID)
                        sql = "INSERT INTO sysusers VALUES (%s, %s, 1)"
                        sqlInput = (inputID, inputType)
                        crsr.execute(sql, sqlInput)
                        crsr.execute("Commit")
            # Resetting SU field
            crsr.execute("SELECT * FROM sysusers")
            result = crsr.fetchall()
            self.SU_result_field.clear()
            self.SU_result_field.insertPlainText("  User ID  |      User Type       | isActive \n")
            for x in result:
                userID = x[0]
                userType = '{:20s}'.format(x[1])
                isActive = str(x[2])
                self.SU_result_field.insertPlainText(" " + userID + " | " + userType + " | " + isActive + "\n")
        except mysql.connector.Error as err:
            print(err)
    # END OF activate_user

    def suspend_User(self): # sets isActive flag for the specified user ID in sysusers
        global crsr
        inputID = self.SU_id_field.text()
        try:
            if(inputID == ""):
                self.SU_Feedback.setText("Error - Incomplete Input")
            else:
                sql = "SELECT * FROM sysusers WHERE id = %s"
                sqlInput = (inputID,)
                crsr.execute(sql, sqlInput)
                result = crsr.fetchall()
                if(result):
                    self.SU_Feedback.setText("Suspending user " + inputID)
                    sql = "UPDATE sysusers SET isActive = 0 WHERE id = %s"
                    sqlInput = (inputID,)
                    crsr.execute(sql, sqlInput)
                    crsr.execute("Commit")
                else:
                    self.SU_Feedback.setText("Error - Incomplete Input")
            # Resetting SU field
            crsr.execute("SELECT * FROM sysusers")
            result = crsr.fetchall()
            self.SU_result_field.clear()
            self.SU_result_field.insertPlainText("  User ID  |      User Type       | isActive \n")
            for x in result:
                userID = x[0]
                userType = '{:20s}'.format(x[1])
                isActive = str(x[2])
                self.SU_result_field.insertPlainText(" " + userID + " | " + userType + " | " + isActive + "\n")
        except mysql.connector.Error as err:
            print(err)
    # END OF suspend_user
    
# END OF AdminScreen

def main(): # Main command line program loop - Halts when desktop window (login/admin) is being used
    try:
        global crsr
        global mydb
        repeat = True
        while(repeat):
            print("-=- Sun Lab Access System -=-")
            print("1. Swipe in/out of the Sun Lab")
            print("2. Access the Access System Menu")
            print("3. Exit the program")
            enter = str(input("Enter the number for command to use: "))
            print("")
            match enter:
                case "1": # User Swipes in/out
                    swipeIn(crsr)
                case "2":
                    adminMenu(crsr) # Access Admin Menu
                    print("")
                    global loginSuccess
                    if(loginSuccess == True):
                        loginSuccess = False
                        showAdminScreen(crsr)
                case "3": # End Program
                    repeat = False
                case default:
                    print("Error incorrect input.")
            print("")
        # End of While Loop (Main command line program loop)
    except mysql.connector.Error as err:
        print(err)
    else:
        crsr.close()
        mydb.close()
# END OF MAIN

#Function to have a user swipe in/out
def swipeIn(crsr):
    try:
        swipe = str(input("Input ID: "))
        while(not swipe[0:1].isnumeric()):
            swipe = swipe[1:]
        swipe = swipe[0:9]
        sql = "SELECT * FROM sysusers WHERE id = %s"
        sqlInput = (swipe,)
        crsr.execute(sql, sqlInput)
        result = crsr.fetchall()
        if (result):
            if(result[0][2] == 1):
                sql = "INSERT INTO accesses VALUES (%s, %s, 1)"
                now = datetime.datetime.utcnow()
                sqlInput = (swipe,now.strftime('%Y-%m-%d %H:%M:%S'))
                crsr.execute(sql,sqlInput)
                print("Swipe successful")
                crsr.execute("Commit")
            else:
                sql = "INSERT INTO accesses VALUES (%s, %s, 0)"
                now = datetime.datetime.utcnow()
                sqlInput = (swipe,now.strftime('%Y-%m-%d %H:%M:%S'))
                crsr.execute(sql,sqlInput)
                print("Swipe unsuccessful - Access Denied")
                crsr.execute("Commit")
        else:
            print("Swipe unsuccessful - Access Denied")
    except mysql.connector.Error as err:
        print(err) 
# END OF swipeIn

# Function to open up the login screen
def adminMenu(crsr): 
    app = QtWidgets.QApplication(sys.argv)
    print("Opening Access System Login Menu")
    login = LoginScreen()
    login.show()
    app.exec()
# END OF adminMenu

# Function to open up the admin screen
def showAdminScreen(crsr):
    app = QtWidgets.QApplication(sys.argv)
    print("Opening Access System Menu")
    admin = AdminScreen()
    admin.show()
    app.exec()
# END OF showAdminScreen

main() # SHOULD ALWAYS BE CALLED AT THE END OF THE CODE
