#!/usr/bin/env python

import logging
import sys
import configparser

from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
from xbox import Xbox

# Testing
import sys, socket, select, time

app = Flask(__name__)
ask = Ask(app, '/')
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

def getArgs():
    config_file = 'config.ini'
    config = configparser.ConfigParser()
    config.read(config_file)

    ip_addr = config.get('XBOX','ipAddress').replace("'","")
    live_id = config.get('XBOX','liveID').replace("'","")

    return ip_addr, live_id

@ask.launch
def main():
    config_file = 'config.ini'
    config = configparser.ConfigParser()
    config.read(config_file)

    ip_addr, live_id = getArgs()

    x = Xbox(live_id, ip_addr)
    x.connect()
    x.send_power()

    print("Xbox should turn on now, pinging to make sure...")
    ping_result = x.send_ping()

    if ping_result:
        print("Ping successful!")
        result_msg = render_template('success')
    else:
        print("Failed to ping Xbox :(")
        result_msg = render_template('failure')

    x.close_socket()
    return question(result_msg)

@app.route('/docker')
def docker():
    ''' Used for testing that the container is accessible as expected '''
    ip_addr, live_id = getArgs()

    x = Xbox(live_id, ip_addr)
    x.connect()
    x.send_power()

    print("Xbox should turn on now, pinging to make sure...")
    ping_result = x.send_ping()

    if ping_result:
        print("Ping successful!")
        result_msg = render_template('success')
    else:
        print("Failed to ping Xbox :(")
        result_msg = render_template('failure')

    x.close_socket()

    return 'works'

@app.route('/ping')
def ping():
    ''' Used for testing to make sure the container is on the host network ''' 
    def send_ping(s):
        s.send(bytearray.fromhex("dd00000a000000000000000400000002"))
        return select.select([s], [], [], 5)[0]

    ip_addr, live_id = getArgs()

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setblocking(0)
    s.bind(("", 0))
    s.connect((ip_addr, 5050))

    ping_result = send_ping(s)

    if ping_result:
        return "Ping successful!"
    else:
        return "Failed to ping Xbox :("

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
