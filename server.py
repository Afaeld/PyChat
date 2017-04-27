# coding: utf-8
import socket
import select
import threading
import errno
import time


def broadcastMessage(listOfClient,message):
    for sendingClient in listOfClient:
            sendingClient.send(message.encode())

if __name__ == '__main__':
    tcpsock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    tcpsock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    tcpsock.bind(("172.26.167.83",1111))
    tcpsock.listen(10)
    listOfClient = []
    listOfId = dict()
    print ("Listening")
    while True:
        try:
            connectionList , wlist, xlist = select.select([tcpsock],[tcpsock],[],0.05)
        except select.error:
            print("disconnect")
            pass
        for connection in connectionList:
            clientConnection, connectionInformation = connection.accept()
            nick = clientConnection.recv(1024)
            listOfClient.append(clientConnection)
            listOfId[clientConnection.fileno()] = nick.decode()
            clientConnection.send("Welcome in the chatRoom".encode()+nick)


        clientsToRead = []
        try:
            clientsToRead, wlist, xlist = select.select(listOfClient,listOfClient,[],0.05)
        except select.error as e:
            if e.errno == errno.WSAECONNRESET:
                print("kek deco")
        else:
            for client in clientsToRead:
                print(listOfId)
                print("receive message")
                fileno = client.fileno()
                try:
                    msg = client.recv(1024).decode()
                    print(msg)
                    for sendingClient in listOfClient:
                        if sendingClient.fileno() != fileno:
                            print("sending to all")
                            msg = "" + str(listOfId[sendingClient.fileno()]) + " : " + msg
                            sendingClient.send(msg.encode())
                except select.error as e:
                    if e.errno == errno.WSAECONNRESET:
                        message = "/!\ " + str(listOfId[client.fileno()]) + " leave the chatroom(disconnection) /!\ "
                        listOfClient.remove(client)
                        client.close()
                        broadcastMessage(listOfClient,message)
                        print("kek deco")
