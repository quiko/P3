import radio
from microbit import *

radio.config(channel=18, data_rate=radio.RATE_2MBIT, group=18)

radio.on()

message = "GOOD INFORMATION"

condition = False

while not condition:
    if message == str(radio.receive_bytes()):
        condition = True
        radio.send_bytes(bytes("1", 'utf8'))
    if not condition:
        display.show(Image('90009:'
                           '09090:'
                           '00900:'
                           '09090:'
                           '90009'))
    else:
        display.show(Image('99999:'
                           '90009:'
                           '90009:'
                           '90009:'
                           '99999'))
    sleep(100)
