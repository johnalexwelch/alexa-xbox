#!/usr/bin/env python

import logging
import sys
import configparser
from xbox import Xbox

def main():
    config_file = 'config.ini'
    config = configparser.ConfigParser()
    config.read(config_file)

    ip_addr = config.get('XBOX','ipAddress').replace("'","")
    live_id = config.get('XBOX','liveID').replace("'","")

    x = Xbox(live_id, ip_addr)
    x.connect()
    x.send_power()

    print("Xbox should turn on now, pinging to make sure...")
    ping_result = x.send_ping()

    if ping_result:
        print("Ping successful!")
        result_msg = 'success'
    else:
        print("Failed to ping Xbox :(")
        result_msg = 'failure'

    x.close_socket()

    return 'works'

if __name__ == "__main__":
    main()
