#!/usr/bin/python
#
# Description : Server to provide a SIP directory
#
# Author : thomas.boutry@x3rus.com
# Licence : GPLv3
# TODO : list of task todo
#   TODO : manage bad json file
# -*- coding: utf-8 -*-
############################################################################

###########
# Modules #

import argparse                                    # Process command line argument
import sys                                         # For return code
import logging                                     # Have a unified logging format
import os                                          # for logs informations
import socket                                      # Socket librairy for tcp connexion
import getpass                                     # get user name running script
import _thread                                     # Threading Client connexion
import json                                        # Load data file with json format


def setLogging(level=logging.WARNING, log_filename=None):
    """ Set x3rus Logging , realy look like syslog :P, Message parsable by Splunk or ELK
    Arguments :
        level : define logging level
        log_filename : specified file name where log information if none use stdout
    Return :
        logging class to use it everywhere
    """

    # Extract information of the system to be able extract information from Splunk
    shortHostname = os.uname()[1].split(".")[0]
    user_running = getpass.getuser()
    pidScript = str(os.getpid())
    scriptName = str(os.path.basename(__file__))

    # Define standard output
    FORMAT = '%(levelname)s: %(asctime)-15s ' + shortHostname + ' X3:' + scriptName + \
             '[' + pidScript + ']: (' + user_running + ') msg:%(message)s'

    # If no file output information to stdout
    if log_filename is None:
        logging.basicConfig(format=FORMAT, level=level)
    else:
        logging.basicConfig(format=FORMAT, level=level, filename=log_filename)

    return logging


class SIPdirectorySrv:
    """
    Server Load json file in memory ,  listening on a TCP socket
    When a client connects, it can make lookup requests.
    It sends one AOR per line. The server responds with the corresponding JSON object.
    The client may send as many requests as it wants, one after the other.
    If a TCP connection is inactive for more than 10 seconds, the server closes it.
    If an AOR cannot be found, the server returns an empty line.
    """

    def __init__(self, socketIP=socket.gethostname(), socketPort=1235):
        """ Initial class
        Arguments :
            socketIP : IP to bind TCP socket
            socketPort : TCP port number
        """

        logging.info("Opening socket : " + socketIP + ":" + str(socketPort))

        # Create socket and bind it to the IP and port in argument
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.bind((socketIP, socketPort))

        # Flag to be able to close server and stop the loop
        self.enable = True

        # Dictionnary of json data , initialisation
        self.dic_sipData = {}

    def loadSIPdataDirectory(self, datafile="../data/regs"):
        """ Load json file for dictionnary

        Return :
            True/False : if the loading work properly
        """
        try:
            # Count entry loaded in memory
            line_num = 1
            for line in open(datafile).readlines():
                # Process each line and add it to a dictionnary , use addressOfRecord as key
                # To facilitate client request
                entry = json.loads(line)
                self.dic_sipData[entry['addressOfRecord']] = entry
                line_num += 1

            # Log number of line loaded
            logging.info("System loaded : " + str(line_num - 1) + " entry")
        except FileNotFoundError:
            return False

        return True

    def processConnection(self, clientsocket, clientaddr):
        """ Process client connexion and request
        Arguments :
            clientsocket : socket of the client
            clientaddr (tuple) : containe client ip and client port
        """

        # Log client connexion
        client_ip, client_port = clientaddr
        logging.info("Accepted connection from: " + client_ip + ":" + str(client_port))

        try:
            # Set timeout to 10 secs after this time socket is close by server
            clientsocket.settimeout(10)

            # Loop information recieved from client
            while True:
                # Read data from client
                data = clientsocket.recv(1024)

                if data == "bye\n" or not data:
                    break
                elif data:
                    # TODO data validation

                    # Extract AOR requested
                    info = self.SearchEntry(data.decode('ascii').strip())

                    # Log information requeste and answer to the client
                    logging.info("Client requested : " + data.decode('ascii').strip())
                    logging.info(" Answer : ")
                    logging.info(info)

                    # return information to the client
                    clientsocket.sendall(bytes(str(info), 'utf8'))

        except socket.timeout:
            clientsocket.close()

        clientsocket.close()

    def SearchEntry(self, aor):
        """ Search in the Address dictionnary information request by client
        Arguments :
            aor : Address of record requested
        Return :
            Json information of the AOR or empty line
        """
        try:
            return self.dic_sipData[aor]
        except KeyError:
            return "\n"

    def AcceptConnection(self, maxQueueConn=5):
        """ Listen and wait connexion
        Arguments:
            maxQueueConn : Max connexion to queue
        """

        # become a server socket
        self.serversocket.listen(maxQueueConn)

        # Loop for every connexion and start thread to manage connexion
        while True:
            try:
                # Log change server status
                logging.info("Server is listening for connections\n")

                # Accept connexion and start a thread to manage it
                clientsocket, clientaddr = self.serversocket.accept()
                _thread.start_new_thread(
                    self.processConnection, (clientsocket, clientaddr))

                # if class have indication to stop processing stop looping
                if self.enable is False:
                    break
            except KeyboardInterrupt:
                logging.info("Closing server socket...")
                break
        self.serversocket.close()

    def closeServer(self):
        """ Stop server , close socket  """
        logging.info("Closing server socket...")
        self.enable = False
        self.serversocket.close()

# END class SIPdirectorySrv:


#########
# Main  #


if __name__ == '__main__':

    # ########################
    # Command Line Arguments #
    parser = argparse.ArgumentParser(description='Sever to provide SIP directory ')
    parser.add_argument('--data', '-d', help='SIP AOR the load ', default="../data/regs")
    parser.add_argument('--ip', '-i', help='define ip to bind service ', default="127.0.0.1")
    parser.add_argument('--log', '-l', help='define log file', default=None)
    parser.add_argument('--port', '-p', type=int, help='define port for tcp listening', default=1234)
    parser.add_argument('--verbose', '-v', action='store_true', help='Unable Verbose mode', default=False)

    args = parser.parse_args()

    # Manage verbose mode
    if args.verbose:
        logLevel = logging.INFO
    else:
        logLevel = logging.WARNING

    # setup logging mode
    setLogging(logLevel, args.log)

    # Start server & load data , if data cannot be load quit
    sipdir = SIPdirectorySrv(args.ip, args.port)
    if sipdir.loadSIPdataDirectory(args.data) is False:
        logging.error('unable load data %s ', args.data)
        sys.exit(1)
    sipdir.AcceptConnection()
