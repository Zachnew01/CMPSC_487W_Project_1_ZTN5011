# Form implementation generated from reading ui file 'loginscreen.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_loginscreen(object):
    def setupUi(self, loginscreen):
        loginscreen.setObjectName("loginscreen")
        loginscreen.resize(231, 117)
        self.centralwidget = QtWidgets.QWidget(parent=loginscreen)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.outputLabel = QtWidgets.QLabel(parent=self.centralwidget)
        self.outputLabel.setText("")
        self.outputLabel.setObjectName("outputLabel")
        self.gridLayout.addWidget(self.outputLabel, 2, 2, 1, 1)
        self.usernameLabel = QtWidgets.QLabel(parent=self.centralwidget)
        self.usernameLabel.setObjectName("usernameLabel")
        self.gridLayout.addWidget(self.usernameLabel, 0, 1, 1, 1)
        self.usernameField = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.usernameField.setObjectName("usernameField")
        self.gridLayout.addWidget(self.usernameField, 0, 2, 1, 1)
        self.passwordLabel = QtWidgets.QLabel(parent=self.centralwidget)
        self.passwordLabel.setObjectName("passwordLabel")
        self.gridLayout.addWidget(self.passwordLabel, 1, 1, 1, 1)
        self.passwordField = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.passwordField.setObjectName("passwordField")
        self.gridLayout.addWidget(self.passwordField, 1, 2, 1, 1)
        self.loginButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.loginButton.setObjectName("loginButton")
        self.gridLayout.addWidget(self.loginButton, 2, 1, 1, 1)
        loginscreen.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(parent=loginscreen)
        self.statusbar.setObjectName("statusbar")
        loginscreen.setStatusBar(self.statusbar)

        self.retranslateUi(loginscreen)
        QtCore.QMetaObject.connectSlotsByName(loginscreen)

    def retranslateUi(self, loginscreen):
        _translate = QtCore.QCoreApplication.translate
        loginscreen.setWindowTitle(_translate("loginscreen", "Login Menu"))
        self.usernameLabel.setText(_translate("loginscreen", "Username:"))
        self.passwordLabel.setText(_translate("loginscreen", "Password"))
        self.loginButton.setText(_translate("loginscreen", "Login"))
