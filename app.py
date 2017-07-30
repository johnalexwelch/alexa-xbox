#!/usr/bin/env python

import logging
import sys
import configparser

from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
from xbox import Xbox

app = Flask(__name__)
ask = Ask(app, '/')
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

@ask.launch
def main():
    config_file = 'config.ini'
    config = configparser.ConfigParser()
    config.read(config_file)

    ip_addr = config.get('XBOX','ipAddress').replace("'","")
    live_id = config.get('XBOX','liveID')

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

if __name__ == "__main__":
    app.run(debug=True)
