#                          __
#                         /\ \
#   ____     __    ___    \_\ \     __   _ __
#  /',__\  /'__`\/' _ `\  /'_` \  /'__`\/\`'__\
# /\__, `\/\  __//\ \/\ \/\ \L\ \/\  __/\ \ \/
# \/\____/\ \____\ \_\ \_\ \___,_\ \____\\ \_\
#  \/___/  \/____/\/_/\/_/\/__,_ /\/____/ \/_/


import radio
from microbit import *
from g18_radio_module import Message

radio.config(channel=18, group=18)

radio.on()

Message.set_key("super secret key")

condition = False

if not Message.establish_connection(is_child=True):  # or False on the parent
    display.scroll("HANDSHAKE FAILED")
    raise SystemExit
else:
    display.show(Image("99999:90009:90009:90009:99999"))

# while not condition:
#     message = Message("GOOD INFORMATION", "info")
#     message.send()
#     try:
#         packet = Message.receive()
#         if int(packet.content) == 1:
#             condition = True
#     except:
#         condition = False
#     if not condition:
#         display.show(Image("90009:09090:00900:09090:90009"))
#     else:
#         display.show(Image("99999:90009:90009:90009:99999"))
#     sleep(100)
