#                     _
#  ___  ___ _ __   __| | ___ _ __
# / __|/ _ \ '_ \ / _` |/ _ \ '__|
# \__ \  __/ | | | (_| |  __/ |
# |___/\___|_| |_|\__,_|\___|_|
#

import radio
from microbit import *
from g18_radio_module import Message

radio.config(channel=18, group=18)

radio.on()

Message.set_key("super secret key")

condition = False

while not condition:
    message = Message("GOOD INFORMATION", "info")
    message.send()
    try:
        packet = Message.receive()
        if int(packet.message_content) == 1:
            condition = True
    except:
        condition = False
    if not condition:
        display.show(Image("90009:09090:00900:09090:90009"))
    else:
        display.show(Image("99999:90009:90009:90009:99999"))
    sleep(100)
