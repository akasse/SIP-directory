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

import argparse                     # command line Args
import time                         # Add some sleep in the code
import socket                       # socket client
from subprocess import Popen        # Start Server application
import sys                          # to exit with good code
import unittest                     # Base unit class
# import threading                  # Originaly try to start server without success


# from server.server import SIPdirectorySrv

#############
# Classe    #

# Create Class to be able to pass parameters
class ParametrizedTestCase(unittest.TestCase):
    """ TestCase classes that want to be parametrized should
        inherit from this class.
        Source : https://eli.thegreenplace.net/2011/08/02/python-unit-testing-parametrized-test-cases/
        Author : Eli Bendersky
    """
    def __init__(self, methodName='runTest', dic_param=None):
        super(ParametrizedTestCase, self).__init__(methodName)
        self.dic_param = dic_param

    @staticmethod
    def parametrize(testcase_klass, dic_param=None):
        """ Create a suite containing all tests taken from the given
            subclass, passing them the parameter 'dic_param'.
        """
        testloader = unittest.TestLoader()
        testnames = testloader.getTestCaseNames(testcase_klass)
        suite = unittest.TestSuite()
        for name in testnames:
            suite.addTest(testcase_klass(name, dic_param=dic_param))
        return suite
# END class ParametrizedTestCase


class ValisationServerSip(ParametrizedTestCase):
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

        if self.dic_param['docker'] is False:
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

        if self.dic_param['docker'] is False:
            # Send terminate signal to the server process
            self.cmdOs_startSrv.kill()

            # wait a little bit and validate process ended
            time.sleep(1)

            # Information if the process still running
            self.cmdOs_startSrv.poll()

#########
# Main  #


if __name__ == '__main__':

    # #######################
    # Command Line Arguments
    parser = argparse.ArgumentParser(description='unittest to validate app')
    parser.add_argument('--docker', '-d', action='store_true', help='Unittest in docker so server already started',
                        default=False)
    args = parser.parse_args()

    # Feed a dictionnary with all parameters give option for future parameters
    dic_testParam = {'docker': args.docker}

    suite = unittest.TestSuite()
    suite.addTest(ParametrizedTestCase.parametrize(ValisationServerSip, dic_testParam))
    return_code = unittest.TextTestRunner(verbosity=9).run(suite)
    if return_code.wasSuccessful() is False:
        sys.exit(9)
