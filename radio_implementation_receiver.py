#                    _
#  _ __ ___  ___ ___(_)_   _____ _ __
# | '__/ _ \/ __/ _ \ \ \ / / _ \ '__|
# | | |  __/ (_|  __/ |\ V /  __/ |
# |_|  \___|\___\___|_| \_/ \___|_|
#

import radio
from microbit import *

radio.config(channel=18, group=18)

radio.on()


def xor_crypt(data, key):
    if isinstance(data, str):
        data = data.encode("utf-8")
    if isinstance(key, str):
        key = key.encode("utf-8")
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))


key = "secret"

message = "GOOD INFORMATION"

condition = False

while not condition:
    # if message == xor_crypt(radio.receive(), key).decode("utf-8"):
    if message == radio.receive():
        condition = True
        radio.send("1")
    if not condition:
        display.show(Image("90009:09090:00900:09090:90009"))
    else:
        display.show(Image("99999:90009:90009:90009:99999"))
    sleep(100)
