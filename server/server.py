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

import argparse                                    # Process command line argument
import sys
# import os
import socket
import _thread
import json
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

        self.enable = True
        self.dic_sipData = {}

        # TODO : Load data

    def loadSIPdataDirectory(self, datafile="../data/regs"):
        """ Load regs information """
        try:
            # TODO ajout try
            line_num = 1
            for line in open(datafile).readlines():
                entry = json.loads(line)
                self.dic_sipData[entry['addressOfRecord']] = entry
                line_num += 1

            print("System loaded : " + str(line_num - 1) + " entry")
        except FileNotFoundError:
            print("file not found :" + datafile + ":")
            return False

        return True

    def processConnection(self, clientsocket, clientaddr):
        """ TODO processConnection doc """
        print("Accepted connection from: ", clientaddr)

        try:
            clientsocket.settimeout(10)

            # Loop information recieved from client
            while True:
                data = clientsocket.recv(1024)

                if data == "bye\n" or not data:
                    break
                elif data:
                    # TODO process with data validation

                    info = self.SearchEntry(data.decode('ascii').strip())
                    print("Client requested : " + data.decode('ascii').strip())
                    print(" Answer : ")
                    print(info)
                    clientsocket.sendall(bytes(str(info), 'utf8'))

        except socket.timeout:
            clientsocket.close()

        clientsocket.close()

    def SearchEntry(self, aor):
        """ TODO """
        try:
            return self.dic_sipData[aor]
        except KeyError:
            return "\n"

    def AcceptConnection(self, maxQueueConn=5):
        """ TODO """

        # become a server socket
        self.serversocket.listen(maxQueueConn)

        while True:
            try:
                print("Server is listening for connections\n")
                clientsocket, clientaddr = self.serversocket.accept()
                _thread.start_new_thread(
                    self.processConnection, (clientsocket, clientaddr))
                if self.enable is False:
                    break
            except KeyboardInterrupt:
                print("Closing server socket...")
                break
        self.serversocket.close()

    def closeServer(self):
        """ """
        print("Closing server socket...")
        self.enable = False
        # self.serversocket.shutdown(1)
        self.serversocket.close()

# END class SIPdirectorySrv:


#########
# Main  #


if __name__ == '__main__':

    # #######################
    # Command Line Arguments
    parser = argparse.ArgumentParser(description='SIP directory ')
    parser.add_argument('--data', '-d', help='SIP AOR the load ', default="../data/regs")
    parser.add_argument('--ip', '-i', help='define ip to bind service ', default="127.0.0.1")
    parser.add_argument('--log', '-l', help='define log file', default="./srv-SIP.log")
    parser.add_argument('--port', '-p', type=int, help='define port for tcp listening', default=1234)
    parser.add_argument('--verbose', '-v', action='store_true', help='Unable Verbose mode', default=False)

    args = parser.parse_args()

    sipdir = SIPdirectorySrv(args.ip, args.port)
    if sipdir.loadSIPdataDirectory(args.data) is False:
        print("ERROR : unable to load " + args.data)
        sys.exit(1)
    sipdir.AcceptConnection()
