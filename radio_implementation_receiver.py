#                    _
#  _ __ ___  ___ ___(_)_   _____ _ __
# | '__/ _ \/ __/ _ \ \ \ / / _ \ '__|
# | | |  __/ (_|  __/ |\ V /  __/ |
# |_|  \___|\___\___|_| \_/ \___|_|
#

import radio
from microbit import *
from g18_radio_module import Message

radio.config(channel=18, group=18)

radio.on()

Message.set_key("super secret key")

condition = False

while not condition:
    message = "GOOD INFORMATION"
    # if message == xor_crypt(radio.receive(), key).decode("utf-8"):
    try:
        packet = Message.receive()
        if message == packet.message_content:
            condition = True
            confirmation = Message("1", "1")
    except:
        condition = False
    if not condition:
        display.show(Image("90009:09090:00900:09090:90009"))
    else:
        display.show(Image("99999:90009:90009:90009:99999"))
    sleep(100)
