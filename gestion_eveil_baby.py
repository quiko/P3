from microbit import *

# ----- SEUILS ISSUS DELA MESURE DE L'ACCELEROMETRE ( voire fichiers de mesurements ) -----

SEUIL_AGITE = 80
SEUIL_TRES_AGITE = 900
TAILLE_FENETRE = 10    # 10 mesures x 100 ms = 1 seconde


historique = []   # on utilsera cette liste dans le calcule de la moyenne glissante de l'acceleration
x_prec, y_prec, z_prec = accelerometer.get_x(), accelerometer.get_y(), accelerometer.get_z()  
etat_precedent = None


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


    # affichage de l'état du bébé si il a changé
    if etat != etat_precedent:
        if etat == "calme":
            display.show(Image.HAPPY)
        elif etat == "agite":
            display.show(Image.SAD)
        else:
            display.show(Image.ANGRY)

        etat_precedent = etat


    sleep(100)  # pause de 100 ms avant la prochaine mesure