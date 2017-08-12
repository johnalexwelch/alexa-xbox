import sys, socket, select, time
from argparse import ArgumentParser

XBOX_PORT = 5050
XBOX_PING = "dd00000a000000000000000400000002"
XBOX_POWER = "dd02001300000010"

py3 = sys.version_info[0] > 2

def getArgs():
    config_file = 'config.ini'
    config = configparser.ConfigParser()
    config.read(config_file)

    ip_addr = config.get('XBOX','ipAddress').replace("'","")
    live_id = config.get('XBOX','liveID').replace("'","")

    return ip_addr, live_id


def main():

    ip_addr, live_id = getArgs()

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setblocking(0)
    s.bind(("", 0))
    s.connect((ip_addr, 5050))

    if isinstance(live_id, str):
        live_id = live_id.encode()
    else:
        live_id = live_id

    power_payload = b'\x00' + chr(len(live_id)).encode() + live_id + b'\x00'
    power_header = b'\xdd\x02\x00' + chr(len(power_payload)).encode() + b'\x00\x00'
    power_packet = power_header + power_payload
    print("Sending power on packets to {0}...".format(args.ip_addr))
    send_power(s, power_packet)

    print("Xbox should turn on now, pinging to make sure...")
    ping_result = send_ping(s)

    if ping_result:
        print("Ping successful!")
    else:
        print("Failed to ping Xbox :(")
        result = ""
        if not args.forever:
            while result not in ("y", "n"):
                result = user_input("Do you wish to keep trying? (y/n): ").lower()
        if args.forever or result == "y":
            print("Sending power packets and pinging until Xbox is on...")
            while not ping_result:
                send_power(s, power_packet)
                ping_result = send_ping(s)
            print("Ping successful!")

    s.close()


def send_power(s, data, times=5):
    for i in range(0, times):
        s.send(data)
        time.sleep(1)


def send_ping(s):
    s.send(bytearray.fromhex(XBOX_PING))
    return select.select([s], [], [], 5)[0]


def user_input(text):
    response = ""

    while response == "":
        if py3:
            response = input(text)
        else:
            response = raw_input(text)

    return response

if __name__ == "__main__":
    main()
