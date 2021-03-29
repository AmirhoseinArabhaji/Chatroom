import socket
from Parser import Parser

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, QObject
from private_message import Ui_ChatWindow

PORT = 10001


class Ui_MainWindow(object):
    def __init__(self, username):
        super(Ui_MainWindow, self).__init__()

        # set attributes
        self.username = username
        self.port = PORT
        self.connect_to_server()

    def setupUi(self, MainWindow):
        # main window configuration
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(800, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(800, 600))
        MainWindow.setMaximumSize(QtCore.QSize(800, 600))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")

        # vertical line configuration
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(540, 0, 20, 561))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line.sizePolicy().hasHeightForWidth())
        self.line.setSizePolicy(sizePolicy)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

        # chat history configuration
        self.chatHistory = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.chatHistory.setEnabled(True)
        self.chatHistory.setGeometry(QtCore.QRect(10, 10, 531, 511))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.chatHistory.setFont(font)
        self.chatHistory.setReadOnly(True)
        self.chatHistory.setObjectName("chatHistory")

        # message box configuration
        self.messageBox = QtWidgets.QLineEdit(self.centralwidget)
        self.messageBox.setGeometry(QtCore.QRect(10, 530, 441, 20))
        self.messageBox.setObjectName("messageBox")

        # send public message button configuration
        self.sendPublicButton = QtWidgets.QPushButton(self.centralwidget)
        self.sendPublicButton.setGeometry(QtCore.QRect(460, 529, 81, 21))
        self.sendPublicButton.setCheckable(False)
        self.sendPublicButton.setObjectName("sendPublicButton")

        # attendees label configuration
        self.attendeesLabel = QtWidgets.QLabel(self.centralwidget)
        self.attendeesLabel.setGeometry(QtCore.QRect(558, 10, 231, 20))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.attendeesLabel.setFont(font)
        self.attendeesLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.attendeesLabel.setObjectName("attendeesLabel")

        # attendees list label configuration
        self.attendeesList = QtWidgets.QListWidget(self.centralwidget)
        self.attendeesList.setGeometry(QtCore.QRect(560, 40, 231, 481))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setUnderline(False)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.attendeesList.setFont(font)
        self.attendeesList.setObjectName("attendeesList")

        # add item to attendees list example
        item = QtWidgets.QListWidgetItem()
        self.attendeesList.addItem(item)

        # send private message button configuration
        self.sendPrivateButton = QtWidgets.QPushButton(self.centralwidget)
        self.sendPrivateButton.setGeometry(QtCore.QRect(561, 529, 231, 21))
        self.sendPrivateButton.setObjectName("sendPrivateButton")

        # menu bar configuration
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 20))
        self.menubar.setObjectName("menubar")
        self.menuMenu = QtWidgets.QMenu(self.menubar)
        self.menuMenu.setObjectName("menuMenu")
        MainWindow.setMenuBar(self.menubar)

        # status bar configuration
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # menu bar action configuration
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.menuMenu.addAction(self.actionExit)
        self.menubar.addAction(self.menuMenu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Chatroom"))
        self.sendPublicButton.setText(_translate("MainWindow", "Send"))
        self.attendeesLabel.setText(_translate("MainWindow", "Attendees"))
        __sortingEnabled = self.attendeesList.isSortingEnabled()
        self.attendeesList.setSortingEnabled(False)
        self.attendeesList.setSortingEnabled(__sortingEnabled)
        self.sendPrivateButton.setText(_translate("MainWindow", "Send Private Message"))
        self.menuMenu.setTitle(_translate("MainWindow", "Menu"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))

        # my code

        # connect buttons to functions
        self.sendPublicButton.clicked.connect(self.sendPublicClicked)
        self.sendPrivateButton.clicked.connect(self.sendPrivateClicked)

        # connect exit action to exit chat
        self.actionExit.triggered.connect(lambda: self.exitChat())

        # join chat
        self.join_chat()

        # show message in status bar
        self.statusbar.showMessage('Connected to server')

    def sendPublicClicked(self):
        """
        send message to server when send clickes
        """
        # get text from text box
        text = self.messageBox.text()
        # clear text box
        self.messageBox.clear()
        # create message and send message
        text_length = len(text.encode('utf-8'))
        msg = f'Public message, length=<{text_length}>:\r\n<{text}>'.encode('utf-8')
        self.sckt.send(msg)

    def sendPrivateClicked(self):
        """
        send private message in a separate window
        """
        # get users list to show in new window
        users = [str(self.attendeesList.item(i).text()) for i in range(self.attendeesList.count())]
        # create an window instance of private message window
        self.window = QtWidgets.QMainWindow()
        # pass socket and list of users to new window
        self.ui = Ui_ChatWindow(self.sckt, users)
        self.ui.setupUi(self.window)
        # show window
        self.window.show()

    def updateChatHistory(self, text):
        # update chat history with new message
        self.chatHistory.appendPlainText(text)

    def updateAttendeesList(self, users):
        # update attendees list with users list
        self.attendeesList.clear()
        for user in users:
            self.attendeesList.addItem(user)

    def exitChat(self):
        # disconnect client from server and close socket
        self.leave_chat()
        self.sckt.close()
        self.statusbar.showMessage('Disconnected')

    def connect_to_server(self):
        # creating a TCP socket
        self.sckt = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        # connect to specified server
        self.sckt.connect((socket.gethostname(), self.port))

        # create a QThread(GUI thread) for listening to messages from server
        self.thread = QThread()
        self.worker = Worker(self.sckt)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.listen_for_message)
        # start server
        self.thread.start()

    def listen_for_message(self, msg):
        msg_obj = Parser(msg)
        # call parse method to parse the message and a get a dictionary of message content
        info = msg_obj.parse()
        # check for different types of message types and do the wanted job
        self.check_type(info)

    def check_type(self, info_dict):
        # get type of message and remove it from dictionary
        msg_type = info_dict.pop('type')

        if msg_type == 'join':
            username = info_dict.get('username')
            msg = f'<{username}> joined the chat room.'
            self.updateChatHistory(msg)
            self.members_list()
            # print(msg)

        elif msg_type == 'welcome':
            username = info_dict.get('username')
            msg = f'Hi <{username}>, welcome to the chat room.'
            self.updateChatHistory(msg)
            self.members_list()
            # print(msg)

        elif msg_type == 'list':
            users = info_dict.get('usernames')
            self.updateAttendeesList(users)
            # print('Here is the list of attendees:')
            # print(','.join(['<' + username + '>' for username in info_dict.get('usernames')]))

        elif msg_type == 'public':
            msg = f'<{info_dict.get("username")}>: {info_dict.get("message")}'
            self.updateChatHistory(msg)
            # print(msg)

        elif msg_type == 'private':
            msg = f'private message from <{info_dict.get("username")}> to you: {info_dict.get("message")}'
            self.updateChatHistory(msg)
            # print(msg)

        elif msg_type == 'leave':
            msg = f'<{info_dict.get("username")}> left the chat room.'
            self.updateChatHistory(msg)
            self.members_list()
            # print(msg)

    def join_chat(self):
        """
        send join message to server
        """
        msg = f'Hello <{self.username}>'.encode('utf-8')
        self.sckt.send(msg)

    def leave_chat(self):
        """
        send leave message to server
        """
        msg = 'Bye.'.encode('utf-8')
        self.sckt.send(msg)

    def members_list(self):
        """
        send list of members to list
        """
        msg = 'Please send the list of attendees.'.encode('utf-8')
        self.sckt.send(msg)


class Worker(QObject):
    """
    Worker class is run on different thread to listen for messages that come from server
    """
    progress = QtCore.pyqtSignal(str)
    finished = QtCore.pyqtSignal()

    def __init__(self, sckt):
        # QThread.__init__(self)
        super(Worker, self).__init__()
        self.sckt = sckt

    def run(self):
        """
        called when thread starts
        """
        # listen to messages in a True loop
        while True:
            msg = self.sckt.recv(1024).decode('utf-8')
            self.progress.emit(msg)
        self.finished.emit()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow('test_username')
    ui.setupUi(MainWindow)
    MainWindow.show()

    sys.exit(app.exec_())
