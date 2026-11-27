#
#                            __
#  _ __    __    ___     __ /\_\  __  __     __   _ __
# /\`'__\/'__`\ /'___\ /'__`\/\ \/\ \/\ \  /'__`\/\`'__\
# \ \ \//\  __//\ \__//\  __/\ \ \ \ \_/ |/\  __/\ \ \/
#  \ \_\\ \____\ \____\ \____\\ \_\ \___/ \ \____\\ \_\
#   \/_/ \/____/\/____/\/____/ \/_/\/__/   \/____/ \/_/


import radio
from microbit import *
from g18_radio_module import Message

radio.config(channel=18, group=18)

radio.on()

Message.set_key("super secret key")

condition = False

if not Message.establish_connection(is_child=False):  # or False on the parent
    display.scroll("HANDSHAKE FAILED")
    raise SystemExit
else:
    display.show(Image("99999:90009:90009:90009:99999"))

# while not condition:
#     message = "GOOD INFORMATION"
#     # if message == xor_crypt(radio.receive(), key).decode("utf-8"):
#     try:
#         packet = Message.receive()
#         if message == packet.content:
#             condition = True
#             confirmation = Message("1", "1")
#     except:
#         condition = False
#     if not condition:
#         display.show(Image("90009:09090:00900:09090:90009"))
#     else:
#         display.show(Image("99999:90009:90009:90009:99999"))
#     sleep(100)
