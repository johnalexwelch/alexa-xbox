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

@ask.launch
def main():
    config_file = 'config.ini'
    config = configparser.ConfigParser()
    config.read(config_file)

    ip_addr = '192.168.86.65'
    live_id = "FD00B5DEA46B35EE"

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
    ''' Used for testing purposes '''
    config_file = 'config.ini'
    config = configparser.ConfigParser()
    config.read(config_file)

    ip_addr = '192.168.86.65'
    live_id = "FD00B5DEA46B35EE"
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

    return "Hello World"

@app.route('/ping')
def ping():
    ''' Send a ping to make sure the networks are talking ''' 
    def send_ping(s):
        s.send(bytearray.fromhex("dd00000a000000000000000400000002"))
        return select.select([s], [], [], 5)[0]

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setblocking(0)
    s.bind(("", 0))
    s.connect(('192.168.86.65', 5050))

    ping_result = send_ping(s)

    if ping_result:
        return "Ping successful!"
    else:
        return "Failed to ping Xbox :("

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
