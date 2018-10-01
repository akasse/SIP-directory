#!/usr/bin/python
#
# Description : Unittest for server SIP directory
#
# Author : thomas.boutry@x3rus.com
# Licence : GPLv3
# TODO :
# -*- coding: utf-8 -*-
############################################################################

###########
# Modules #

import time                         # Add some sleep in the code
import socket                       # socket client
from subprocess import Popen        # Start Server application
import unittest                     # Base unit class
# import threading                  # Originaly try to start server without success


# from server.server import SIPdirectorySrv

#############
# Classe    #


class ValisationServerSip(unittest.TestCase):
    """ Unittest to validate SIPdirectorySrv
    Unit test is self content , start server and performe validation
    """

    ########
    # Vars #
    bind_ip = '127.0.0.1'               # Server ip to communicate
    bind_port = 1234                    # Port to communicate
    data_to_load = './data/regs'        # SIP file to load

    def setUp(self):
        """ Prerequesite for each test , start server and wait 1 sec to be sure everything
        is initialise , argumente to use logfile
        """

        # I start a process , Originaly I tried to use python class to start server , I had issue
        # to stop the thread in the teardown method , server continue listen indefinitly
        # Because I'm short of time I switch method to go forward , ticket #10 open for that
        self.cmdOs_startSrv = Popen(['python3', 'server/server.py', '-i', self.bind_ip, '-l', './logfile',
                                    '-p', str(self.bind_port), '-d', self.data_to_load, '-v'])

        # Wait for initialisation
        time.sleep(1)

    def request_aor(self, aor):
        """ Method for a single AOR request
        Arguments :
            aor : Address Of Record to ask to the server
        Return :
            Data recieved by the server
        """
        # connect fake test client
        fake_client = socket.socket()
        fake_client.settimeout(2)       # Short timeout for testing
        fake_client.connect((self.bind_ip, self.bind_port))

        # Send request to server
        fake_client.send(bytes(aor, 'utf-8'))
        data = fake_client.recv(1024)
        fake_client.close()

        # Return data recieved by server
        return data

    def test_01_SocketConnection(self):
        """ First Test : validating TCP connexion work """

        # This is our fake test client that is just going to attempt a connect and disconnect
        fake_client = socket.socket()
        fake_client.settimeout(1)         # Short timeout for testing
        fake_client.connect((self.bind_ip, self.bind_port))

        fake_client.close()

    def test_02_RequestAOR(self):
        """ Second Test : Request one AOR existing in the directory  """

        data = self.request_aor('0142e2fa3543cb32bf000100620002')
        # Confirm AOR in the answer
        assert("0142e2fa3543cb32bf000100620002" in data.decode('ascii'))

    def test_03_Wrong_RequestAOR(self):
        """ Third Test : Request a wrong AOR """
        data = self.request_aor('not_a_good_one')
        assert("0142e2fa3543cb32bf000100620002" not in data.decode('ascii'))

    def test_04_RequestAOR_3_time(self):
        """ fourth Test : make multiple AOR request """

        # Establish a connexion to the server
        fake_client = socket.socket()
        fake_client.settimeout(5)
        fake_client.connect((self.bind_ip, self.bind_port))

        # Request a good AOR
        fake_client.send(bytes('0142e2fa3543cb32bf000100620002', 'utf-8'))
        data = fake_client.recv(1024)
        assert("0142e2fa3543cb32bf000100620002" in data.decode('ascii'))

        # Request a wrong AOR
        fake_client.send(bytes('not_a_good_one', 'utf-8'))
        data = fake_client.recv(1024)
        assert("not_a_good_one" not in data.decode('ascii'))

        # Request a good AOR
        fake_client.send(bytes('0148c1f489badb837d000100620002', 'utf-8'))
        data = fake_client.recv(1024)
        assert("0148c1f489badb837d000100620002" in data.decode('ascii'))

        # Close client connexion
        fake_client.close()

    def test_05_timeout_10_sec(self):
        """ fifth Test : validate server timeout after 10 second
        I have issue to perform this test a ticket is open #5
        """
        print("Need to be done issue #5")

    def tearDown(self):
        """ Close server after test , as mention threading was not a success so I kill the server """
        # Send terminate signal to the server process
        self.cmdOs_startSrv.kill()

        # wait a little bit and validate process ended
        time.sleep(1)

        # Information if the process still running
        self.cmdOs_startSrv.poll()

#########
# Main  #


if __name__ == '__main__':
    # Verbosity to 9 to view each test Status
    unittest.main(verbosity=9)
