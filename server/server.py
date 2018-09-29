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
# import re


class SIPdirectorySrv:
    """
    TODO: doc
    """

    def __init__(self, socketIP=socket.gethostname(), socketPort=1234):
        """ TODO """

        # TODO : Add socketIP and socketPort
        print("Opening socket...")
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # bind the socket to a public host, and a well-known port
        self.serversocket.bind((socketIP, socketPort))

        # TODO : Load data

    def processConnection(self, clientsocket, clientaddr):
        """ TODO processConnection doc """
        print("Accepted connection from: ", clientaddr)

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
            # Ctrl+C # FIXME: vraci "raise error(EBADF, 'Bad file descriptor')"
            except KeyboardInterrupt:
                print("Closing server socket...")
                break

# END class SIPdirectorySrv:


#########
# Main  #


if __name__ == '__main__':

        sipdir = SIPdirectorySrv()
        sipdir.AcceptConnection()
