#!/usr/bin/python
#
# Description : Server to provide a SIP directory
#
# Author : thomas.boutry@x3rus.com
# Licence : GPLv3
# TODO :
# -*- coding: utf-8 -*-
############################################################################

###########
# Modules #

# import argparse                                    # Process command line argument
# import sys
# import os
import socket
import _thread
import json
from struct import *
# import re


class SIPdirectorySrv:
    """
    TODO: doc
    """

    def __init__(self, socketIP=socket.gethostname(), socketPort=1235):
        """ TODO """

        # TODO : Add socketIP and socketPort
        print("Opening socket...")
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # bind the socket to a public host, and a well-known port
        self.serversocket.bind((socketIP, socketPort))

        self.dic_sipData = {}

        # TODO : Load data

    def loadSIPdataDirectory(self, datafile="../data/regs"):
        """ Load regs information """

        # TODO ajout try
        line_num = 1
        for line in open(datafile).readlines():
            entry = json.loads(line)
            self.dic_sipData[entry['addressOfRecord']] = entry
            line_num += 1

        print("System loaded : " + str(line_num - 1) + " entry")

    def processConnection(self, clientsocket, clientaddr):
        """ TODO processConnection doc """
        print("Accepted connection from: ", clientaddr)

        # Loop information recieved from client
        while True:
            data = clientsocket.recv(1024)

            if data == "bye\n" or not data:
                break
            elif data:
                dataProcessed = False
                # TODO process with data validation

                dataProcessed = True
                info = self.SearchEntry(data.decode('ascii').strip())
                print("Client requested : " + data.decode('ascii').strip())
                print(" Answer : ")
                print(info)
                self.send_sock_msg(clientsocket, bytes(
                                    str(info), 'utf8'))
                if dataProcessed is False:
                    print("bad CMD recieved :", str(data))
                    clientsocket.send(
                        bytes("Srv : Not processing, BAD CMD", 'utf8'))

        clientsocket.close()

    def SearchEntry(self, aor):
        """ TODO """
        try:
            return self.dic_sipData[aor]
        except KeyError:
            return ""

    def AcceptConnection(self, maxQueueConn=5):
        """ TODO """

        # become a server socket
        self.serversocket.listen(5)

        while True:
            try:
                print("Server is listening for connections\n")
                clientsocket, clientaddr = self.serversocket.accept()
                _thread.start_new_thread(
                    self.processConnection, (clientsocket, clientaddr))
            except KeyboardInterrupt:
                print("Closing server socket...")
                break

    def send_sock_msg(self, sock, message):
        """ TODO doc send_sock_msg """
        # Prefix each message with a 4-byte length (network byte order)
        message = pack('>I', len(message)) + message
        sock.sendall(message)


# END class SIPdirectorySrv:


#########
# Main  #


if __name__ == '__main__':

        sipdir = SIPdirectorySrv("127.0.0.1", 1234)
        sipdir.loadSIPdataDirectory()
        sipdir.AcceptConnection()
