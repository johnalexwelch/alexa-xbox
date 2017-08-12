#!/usr/bin/env python
import socket, time, select

class Xbox(object):
    """ An Xbox one connection.

    Properties:
        live_id (str): The ID tied to the user's Xbox Live account
        ip_addr (str): The LAN ip address to the Xbox One
        xbox_port (int): The port the router was forwarded to
        xbox_ping (str): 'Turn On' message to the Xbox One
        s (obj): Comes from the socket library and handels the connection

    """
    def __init__(self, live_id, ip_addr):
        """
        Returns a connection object for the given
        Xbox One parameters (ip address and live id)
        """
        self.live_id = live_id
        self.ip_addr = ip_addr
        self.xbox_port = 5050
        self.xbox_ping = "dd00000a000000000000000400000002"
        self.s = ''
        print(self.live_id)
        print(self.ip_addr)

    def connect(self):
        """
        Uses the socket library to create a connection to
        the Xbox One
        """
        self.encode_live_id()
        self.build_power_packet()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.setblocking(0)
        self.s.bind(("", 0))
        self.s.connect((self.ip_addr, self.xbox_port))

    def encode_live_id(self):
        """
        Handles the necessary encoding of the Xbox One id
        to be used when building the power packet binary
        """
        if isinstance(self.live_id, str):
            self.live_id = self.live_id.encode()
        return self.live_id

    def send_power(self, times=5):
        """
        Sends the power packet to the connection. Tries it
        5 times.
        """
        for i in range(0, times):
            self.s.send(self.power_packet)
            time.sleep(1)

    def send_ping(self):
        """
        Sends a ping to the Xbox One to make sure the
        machine was successfully turned on
        """
        self.s.send(bytearray.fromhex(self.xbox_ping))
        return select.select([self.s], [], [], 5)[0]

    def build_power_packet(self):
        """
        Builds the power packet to be sent to the Xbox One
        """
        power_payload = b'\x00' + chr(len(self.live_id)).encode() + self.live_id + b'\x00'
        power_header = b'\xdd\x02\x00' + chr(len(power_payload)).encode() + b'\x00\x00'
        self.power_packet = power_header + power_payload
        return self.power_packet

    def close_socket(self):
        """
        Closes the socket connection
        """
        self.s.close()
