from microbit import *
from g18_radio_module import Message
import radio
import music


radio.config(channel=18, group=18)
radio.on()
Message.set_key("super secret key")


dernier_envoi = 0            
etat_affiche = None  
chute = False  # pour indiquer si une chute a été détectée



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
        dernier_envoi = running_time()

        if etat_bebe == "chute":
            chute = True
            display.show(Image.SKULL)
            music.play(music.WAWAWAWAA, wait=False)  

        elif etat_bebe != etat_affiche and not chute:
    
            if etat_bebe == "calme":
                display.show(Image.HAPPY)
                music.stop()
            elif etat_bebe == "agite":
                display.show(Image.SAD)
                music.play(music.PYTHON, wait=False)
            elif etat_bebe == "tres agite":
                display.show(Image.ANGRY)
                music.play(music.BADDY, wait=False)
            etat_affiche = etat_bebe
    if chute and button_a.was_pressed():  # si le parent appuie sur le bouton A après une chute
        chute = False
        display.show(Image.ASLEEP)
        etat_affiche = None
    if (running_time() - dernier_envoi > 15000 and etat_affiche != "perdu" and not chute):  # pas de messages depuis 15 secondes
        display.show(Image.CONFUSED)
        music.stop()
        etat_affiche = "perdu"

    sleep(20) 
