from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ChatWindow(object):
    def __init__(self, sckt, users):
        super(Ui_ChatWindow, self).__init__()

        # set attributes
        self.sckt = sckt
        self.users = users
        self.checkBoxesList = []

    def setupUi(self, ChatWindow):
        # main window configuration
        ChatWindow.setObjectName("ChatWindow")
        ChatWindow.setEnabled(True)
        ChatWindow.resize(600, 400)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ChatWindow.sizePolicy().hasHeightForWidth())
        ChatWindow.setSizePolicy(sizePolicy)
        ChatWindow.setMinimumSize(QtCore.QSize(600, 400))
        ChatWindow.setMaximumSize(QtCore.QSize(600, 400))
        self.centralwidget = QtWidgets.QWidget(ChatWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")

        # text box configuration
        self.textMessage = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.textMessage.setGeometry(QtCore.QRect(10, 40, 321, 291))
        self.textMessage.setObjectName("textMessage")

        # vertical list for attendees
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(340, 40, 251, 311))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        # send button configuration
        self.sendButton = QtWidgets.QPushButton(self.centralwidget)
        self.sendButton.setGeometry(QtCore.QRect(10, 340, 62, 19))
        self.sendButton.setObjectName("sendButton")

        # select attendees label
        self.selectAttendees = QtWidgets.QLabel(self.centralwidget)
        self.selectAttendees.setGeometry(QtCore.QRect(338, 10, 251, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.selectAttendees.setFont(font)
        self.selectAttendees.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.selectAttendees.setObjectName("selectAttendees")

        # write message label
        self.writeMessage = QtWidgets.QLabel(self.centralwidget)
        self.writeMessage.setGeometry(QtCore.QRect(10, 10, 251, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.writeMessage.setFont(font)
        self.writeMessage.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.writeMessage.setObjectName("writeMessage")

        ChatWindow.setCentralWidget(self.centralwidget)
        # self.menubar = QtWidgets.QMenuBar(ChatWindow)
        # self.menubar.setGeometry(QtCore.QRect(0, 0, 600, 20))
        # self.menubar.setObjectName("menubar")
        # ChatWindow.setMenuBar(self.menubar)
        # self.statusbar = QtWidgets.QStatusBar(ChatWindow)
        # self.statusbar.setObjectName("statusbar")
        # ChatWindow.setStatusBar(self.statusbar)
        self.actionExit = QtWidgets.QAction(ChatWindow)
        self.actionExit.setObjectName("actionExit")

        self.retranslateUi(ChatWindow)
        QtCore.QMetaObject.connectSlotsByName(ChatWindow)

    def retranslateUi(self, ChatWindow):
        _translate = QtCore.QCoreApplication.translate
        ChatWindow.setWindowTitle(_translate("ChatWindow", "Chatroom"))
        # self.checkBox.setText(_translate("ChatWindow", "CheckBox"))
        self.sendButton.setText(_translate("ChatWindow", "Send"))
        self.selectAttendees.setText(_translate("ChatWindow", "Select attendees"))
        self.writeMessage.setText(_translate("ChatWindow", "Write Message"))
        self.actionExit.setText(_translate("ChatWindow", "Exit"))

        # my code
        self.sendButton.clicked.connect(self.sendButtonClicked)

        # create a list of users with checkbox for choosing theme
        for user in self.users:
            checkBox = QtWidgets.QCheckBox(user, self.verticalLayoutWidget)
            self.verticalLayout.addWidget(checkBox)
            self.checkBoxesList.append(checkBox)

    def sendButtonClicked(self):
        usersToSend = []
        # get checked users list
        for checkBox in self.checkBoxesList:
            if checkBox.isChecked():
                usersToSend.append(checkBox.text())
        # get message from textbox
        text = self.textMessage.toPlainText()
        # clear text from text box
        self.textMessage.clear()
        # create private message and send to server
        text_length = len(text.encode('utf-8'))
        msg = f'Private message, length=<{text_length}> to '
        msg += ','.join('<' + username + '>' for username in usersToSend) + f':\r\n<{text}>'
        self.sckt.send(msg.encode('utf-8'))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ChatWindow = QtWidgets.QMainWindow()
    ui = Ui_ChatWindow(None, [])
    ui.setupUi(ChatWindow)
    ChatWindow.show()

    sys.exit(app.exec_())
