#!/usr/bin/python
#
# Description : Unittest for server
#
# Author : thomas.boutry@x3rus.com
# Licence : GPLv3
# TODO :
# -*- coding: utf-8 -*-
############################################################################

###########
# Modules #

import unittest
# import threading
import time
import socket

from subprocess import Popen

# from server.server import SIPdirectorySrv

#############
# Classe    #


class ValisationServerSip(unittest.TestCase):
    """ """
    def setUp(self):
        # TODO add comment

        self.cmdOs_startSrv = Popen(['python', 'server/server.py'])
        time.sleep(1)

    def request_aor(self, aor):
        # This is our fake test client that is just going to attempt a connect and disconnect
        fake_client = socket.socket()
        fake_client.settimeout(1)
        fake_client.connect(('127.0.0.1', 1234))

        fake_client.send(bytes(aor, 'utf-8'))
        data = fake_client.recv(1024)
        fake_client.close()
        return data

    def test_01_SocketConnection(self):

        # This is our fake test client that is just going to attempt a connect and disconnect
        fake_client = socket.socket()
        fake_client.settimeout(1)
        fake_client.connect(('127.0.0.1', 1234))

        # TODO check
        # self.sipSrv.closeServer()
        fake_client.close()

    def test_02_RequestAOR(self):
        """ Request an AOR """
        data = self.request_aor('0142e2fa3543cb32bf000100620002')
        assert("0142e2fa3543cb32bf000100620002" in data.decode('ascii'))

    def test_03_Wrong_RequestAOR(self):
        """ Request an AOR """
        data = self.request_aor('not_a_good_one')
        assert("0142e2fa3543cb32bf000100620002" not in data.decode('ascii'))

    def test_04_RequestAOR_3_time(self):
        """ Request an AOR """
        fake_client = socket.socket()
        fake_client.settimeout(1)
        fake_client.connect(('127.0.0.1', 1234))

        fake_client.send(bytes('0142e2fa3543cb32bf000100620002', 'utf-8'))
        data = fake_client.recv(1024)
        assert("0142e2fa3543cb32bf000100620002" in data.decode('ascii'))

        fake_client.send(bytes('not_a_good_one', 'utf-8'))
        data = fake_client.recv(1024)
        assert("not_a_good_one" not in data.decode('ascii'))

        fake_client.send(bytes('0148c1f489badb837d000100620002', 'utf-8'))
        data = fake_client.recv(1024)
        assert("0148c1f489badb837d000100620002" in data.decode('ascii'))

        fake_client.close()

    def tearDown(self):
        # Make sure server thread finishes
        self.cmdOs_startSrv.kill()
        # TODO : ugly fix just to validate
        time.sleep(1)

        # Information if the process still running
        self.cmdOs_startSrv.poll()

#########
# Main  #


if __name__ == '__main__':
    unittest.main(verbosity=9)
