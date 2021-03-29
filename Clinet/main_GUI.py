from PyQt5 import QtCore, QtGui, QtWidgets
from public_chat import Ui_MainWindow


class Ui_WelcomeWindow(object):
    def setupUi(self, WelcomeWindow):
        # main window configuration
        WelcomeWindow.setObjectName("WelcomeWindow")
        WelcomeWindow.setEnabled(True)
        WelcomeWindow.resize(800, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(WelcomeWindow.sizePolicy().hasHeightForWidth())
        WelcomeWindow.setSizePolicy(sizePolicy)
        WelcomeWindow.setMinimumSize(QtCore.QSize(800, 600))
        WelcomeWindow.setMaximumSize(QtCore.QSize(800, 600))
        self.centralwidget = QtWidgets.QWidget(WelcomeWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")

        # welcome label widget
        self.welcomeLabel = QtWidgets.QLabel(self.centralwidget)
        self.welcomeLabel.setGeometry(QtCore.QRect(0, 160, 801, 71))
        font = QtGui.QFont()
        font.setPointSize(30)
        self.welcomeLabel.setFont(font)
        self.welcomeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.welcomeLabel.setObjectName("welcome")

        # enter username label configuration
        self.usernameLabel = QtWidgets.QLabel(self.centralwidget)
        self.usernameLabel.setGeometry(QtCore.QRect(250, 270, 95, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.usernameLabel.setFont(font)
        self.usernameLabel.setObjectName("usernameLabel")

        # username text edit configuration
        self.usernameText = QtWidgets.QLineEdit(self.centralwidget)
        self.usernameText.setGeometry(QtCore.QRect(350, 280, 191, 20))
        self.usernameText.setObjectName("usernameText")

        # join button configuration
        self.joinButton = QtWidgets.QPushButton(self.centralwidget)
        self.joinButton.setGeometry(QtCore.QRect(350, 340, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.joinButton.setFont(font)
        self.joinButton.setObjectName("joinButton")
        WelcomeWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(WelcomeWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 20))
        self.menubar.setObjectName("menubar")
        WelcomeWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(WelcomeWindow)
        self.statusbar.setObjectName("statusbar")
        WelcomeWindow.setStatusBar(self.statusbar)
        self.actionExit = QtWidgets.QAction(WelcomeWindow)
        self.actionExit.setObjectName("actionExit")

        self.retranslateUi(WelcomeWindow)
        QtCore.QMetaObject.connectSlotsByName(WelcomeWindow)

    def retranslateUi(self, WelcomeWindow):
        _translate = QtCore.QCoreApplication.translate
        WelcomeWindow.setWindowTitle(_translate("WelcomeWindow", "Chatroom"))
        self.welcomeLabel.setText(_translate("WelcomeWindow", "Welcome to Chatroom"))
        self.usernameLabel.setText(_translate("WelcomeWindow", "Enter username:"))
        self.joinButton.setText(_translate("WelcomeWindow", "Join"))
        self.actionExit.setText(_translate("WelcomeWindow", "Exit"))

        # my code
        self.joinButton.clicked.connect(self.joinClicked)

    def joinClicked(self):
        # get username from Line edit
        username = self.usernameText.text()
        # create object of public chat window and pass the username and open window
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow(username)
        self.ui.setupUi(self.window)
        self.window.show()
        # hide welcome window
        WelcomeWindow.hide()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    WelcomeWindow = QtWidgets.QMainWindow()
    ui = Ui_WelcomeWindow()
    ui.setupUi(WelcomeWindow)
    WelcomeWindow.show()

    sys.exit(app.exec_())
