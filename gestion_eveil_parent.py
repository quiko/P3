from microbit import *
from g18_radio_module import Message
import radio
import music


radio.config(channel=18, group=18)
radio.on()
Message.set_key("super secret key")






# en attente d'un message du bébé, on affiche un petit bonhomme endormi
display.show(Image.ASLEEP)

# detecter un message de la part du bébé
while True:
    try:
        packet = Message.receive()
    except Exception:
        packet = None

# Afin d'éviter la saturation de la memoire, on vide les onces mémorisées
    if len(Message._seen_nonces) > 5:
        Message._seen_nonces.clear()

    if packet is not None and packet.type == 2:  # si le message est de type état du bébé
        etat_bebe = packet.content
        if etat_bebe == "calme":
            display.show(Image.HAPPY)
            music.stop()
        elif etat_bebe == "agite":
            display.show(Image.SAD)
            music.play(music.PYTHON, wait=False)
        elif etat_bebe == "tres agite":
            display.show(Image.ANGRY)
            music.play(music.BADDY, wait=False)

