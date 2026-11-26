from microbit import *
import music
import radio
from g18_radio_module import Message



radio.config(channel=18, group=18)
radio.on()      
Message.set_key("super secret key")


# Musique pour calmer le bébé
tune = [
    "C4:4", "D", "E", "C",
    "C", "D", "E", "C",
    "E", "F", "G:8",
    "E:4", "F", "G:8",
    "G4:2", "A", "G", "F", "E:4", "C:4",
    "G4:2", "A", "G", "F", "E:4", "C:4",
    "C4:4", "G3", "C4:8",
    "C4:4", "G3", "C4:8",
]

# ----- SEUILS ISSUS DELA MESURE DE L'ACCELEROMETRE ( voire fichiers de mesurements ) -----

SEUIL_AGITE = 80
SEUIL_TRES_AGITE = 900
TAILLE_FENETRE = 10    # 10 mesures x 100 ms = 1 seconde

HEARTBEAT = 5000  # Envoi d'un message toutes les 5 secondes pour indiquer que le bébé est toujours là
TYPE_MESSAGE = 2  # Type de message pour l'état du bébé, 1 c'est pour les handshake


historique = []   # on utilsera cette liste dans le calcule de la moyenne glissante de l'acceleration
x_prec, y_prec, z_prec = accelerometer.get_x(), accelerometer.get_y(), accelerometer.get_z()  
etat_precedent = None
dernier_envoi = 0


while True:
    x,y,z = accelerometer.get_x(), accelerometer.get_y(), accelerometer.get_z()

    # calcul de la variation d'acceleration
    variation = abs(x - x_prec) + abs(y - y_prec) + abs(z - z_prec)
    x_prec, y_prec, z_prec = x, y, z

    # ajout de la variation dans l'historique
    historique.append(variation)
    if len(historique) > TAILLE_FENETRE:
        historique.pop(0)  # on supprime le plus ancien élément pour garder la taille de la fenêtre constante   

    # calcul de la moyenne glissante
    moyenne = sum(historique) / len(historique)

    # détermination de l'état du bébé
    if moyenne < SEUIL_AGITE:
        etat = "calme"
    elif moyenne < SEUIL_TRES_AGITE:
        etat = "agite"
    else:
        etat = "tres agite"


    # affichage de l'état du bébé s'il a changé
    if etat != etat_precedent:
        if etat == "calme":
            display.show(Image.HAPPY)
            music.stop()

        elif etat == "agite":
            display.show(Image.SAD)
            music.play(tune, wait=False)

        else:
            display.show(Image.ANGRY)
            music.play(tune, wait=False)

        # dès que l'état change, on envoie un message au parent
        Message(etat, TYPE_MESSAGE).send()
        dernier_envoi = running_time()  # on met à jour le temps du dernier envoi

        # mise à jour de l'état précédent
        etat_precedent = etat

    # si pas de changement d'état, on envoie un message toutes les 5 secondes pour indiquer que le bébé est toujours là
    else:
        if running_time() - dernier_envoi > HEARTBEAT:  # toutes les 5 secondes
            Message(etat, TYPE_MESSAGE).send()
            dernier_envoi = running_time()  # on met à jour le temps du dernier envoi

    sleep(100)  # pause de 100 ms avant la prochaine mesure