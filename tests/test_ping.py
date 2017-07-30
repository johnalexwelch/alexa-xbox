#!/usr/bin/env python

import unittest
import configparser
from xbox import Xbox

class TestPing(unittest.TestCase):
    def setUp(self):
        config_file = 'config.ini'
        config = configparser.ConfigParser()
        config.read(config_file)
        self.ip_addr = config.get('TEST','ipAddress').replace("'","")
        self.live_id = config.get('XBOX','liveID')

    def test_sendPing(self):
        ping = Xbox(self.live_id, self.ip_addr)
        self.assertTrue(ping.send_ping)

if __name__ == '__main__':
    unittest.main()
