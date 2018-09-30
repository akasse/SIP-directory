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
        # TODO add comment
        self.sipSrv = SIPdirectorySrv('127.0.0.1', 1234)
        self.sipSrv.loadSIPdataDirectory('./data/regs')
        self.server_thread = threading.Thread(target=self.sipSrv.AcceptConnection)
        self.server_thread.start()

    def test_01_SocketConnection(self):

        # On my computer, 0.0000001 is the minimum sleep time or the
        # client might connect before server thread binds and listens
        # Other computers will differ. I wanted a low number to make tests fast
        time.sleep(0.000001)

        # This is our fake test client that is just going to attempt a connect and disconnect
        fake_client = socket.socket()
        fake_client.settimeout(1)
        fake_client.connect(('127.0.0.1', 1234))

        # TODO check
        self.sipSrv.closeServer()
        fake_client.close()

    def tearDown(self):
        # Make sure server thread finishes
        self.sipSrv.closeServer()
        self.server_thread.join()

#########
# Main  #


if __name__ == '__main__':
    unittest.main(verbosity=5)
