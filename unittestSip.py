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
import threading
import time
import socket

from server.server import SIPdirectorySrv

#############
# Classe    #


class ValisationServerSip(unittest.TestCase):
    """ """
    def setUp(self):
        # Start game server in a background thread
        sipSrv = SIPdirectorySrv('127.0.0.1', 1234)
        sipSrv.loadSIPdataDirectory('./data/regs')
        self.thread_event = threading.Event()
        self.server_thread = threading.Thread(target=sipSrv.AcceptConnection, args=(1, self.thread_event))
        self.server_thread.start()

        print("toto")

    def test_01_SocketConnection(self):
        # On my computer, 0.0000001 is the minimum sleep time or the
        # client might connect before server thread binds and listens
        # Other computers will differ. I wanted a low number to make tests fast
        time.sleep(0.000001)

        # This is our fake test client that is just going to attempt a connect and disconnect
        fake_client = socket.socket()
        fake_client.settimeout(1)
        fake_client.connect(('127.0.0.1', 1234))
        fake_client.close()

    def tearDown(self):
        # Make sure server thread finishes
        self.thread_event.set()

#########
# Main  #


if __name__ == '__main__':
    unittest.main()
