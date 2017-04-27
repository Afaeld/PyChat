import sys
from PyQt5 import QtCore, QtGui, uic,QtWidgets
from threading import Thread
import socket
import qdarkstyle

qtCreatorFile = "mainwindow.ui"  # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class receiveMessageHandler(Thread):
    def __init__(self,socket,app):
        Thread.__init__(self)
        self.socket = socket
        self.app = app

    def run(self):
        while True:
            message = s.recv(1024).decode()
            self.app.messageTextBrowser.append(message)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self,s):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.socket = s
        self.sendButton.clicked.connect(self.sendMessage)

    def sendMessage(self):
        print("trigger")
        message = str(self.messageTextEdit.toPlainText())
        self.socket.send(message.encode())
        self.messageTextBrowser.append("You : "+message)
        self.messageTextEdit.clear()
    def closeEvent(self,event):
        self.socket.close()


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("172.26.167.83", 1111))
    nickname = "bob"
    s.send(nickname.encode())
    returnMessage = s.recv(1024)
    print(returnMessage)

    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    window = MyApp(s)
    messageHandler = receiveMessageHandler(s, window)
    try:
        messageHandler.start()
    except Exception:
        messageHandler.join()
        s.close()
    window.show()
    # nickname = input("Enter nickname : ")

    #while True:
     #   message = input(">> ")
     #   s.send(message)
    sys.exit(app.exec_())