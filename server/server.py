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
import logging                                     # Have a unified logging format
import os                                          # for logs informations
import socket
import getpass                                     # get user name running script
import _thread
import json
# import re


def setLogging(level=logging.WARNING, log_filename=None):
    """ Set x3rus Logging , realy look like syslog :P, Message parsable by Splunk or ELK """
    shortHostname = os.uname()[1].split(".")[0]
    user_running = getpass.getuser()
    pidScript = str(os.getpid())
    scriptName = str(os.path.basename(__file__))

    FORMAT = '%(levelname)s: %(asctime)-15s ' + shortHostname + ' X3:' + scriptName + \
             '[' + pidScript + ']: (' + user_running + ') msg:%(message)s'
    if log_filename is None:
        logging.basicConfig(format=FORMAT, level=level)
    else:
        logging.basicConfig(format=FORMAT, level=level, filename=log_filename)

    return logging


class SIPdirectorySrv:
    """
    TODO: doc
    """

    def __init__(self, socketIP=socket.gethostname(), socketPort=1235):
        """ TODO """

        # TODO : Add socketIP and socketPort
        logging.info("Opening socket...")
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

            logging.info("System loaded : " + str(line_num - 1) + " entry")
        except FileNotFoundError:
            return False

        return True

    def processConnection(self, clientsocket, clientaddr):
        """ TODO processConnection doc """
        client_ip, client_port = clientaddr
        logging.info("Accepted connection from: " + client_ip + ":" + str(client_port))

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
                    logging.info("Client requested : " + data.decode('ascii').strip())
                    logging.info(" Answer : ")
                    logging.info(info)
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
                logging.info("Server is listening for connections\n")
                clientsocket, clientaddr = self.serversocket.accept()
                _thread.start_new_thread(
                    self.processConnection, (clientsocket, clientaddr))
                if self.enable is False:
                    break
            except KeyboardInterrupt:
                logging.info("Closing server socket...")
                break
        self.serversocket.close()

    def closeServer(self):
        """ """
        logging.info("Closing server socket...")
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
    parser.add_argument('--log', '-l', help='define log file', default=None)
    parser.add_argument('--port', '-p', type=int, help='define port for tcp listening', default=1234)
    parser.add_argument('--verbose', '-v', action='store_true', help='Unable Verbose mode', default=False)

    args = parser.parse_args()

    if args.verbose:
        logLevel = logging.INFO
    else:
        logLevel = logging.WARNING

    setLogging(logLevel, args.log)

    sipdir = SIPdirectorySrv(args.ip, args.port)
    if sipdir.loadSIPdataDirectory(args.data) is False:
        logging.error('unable load data %s ', args.data)
        sys.exit(1)
    sipdir.AcceptConnection()
