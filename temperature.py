from microbit import *
import music
import speech

def alerte(danger):
    if danger == 0:
        display.show(Image.HAPPY)
    if danger == 1:
        music.play(['b3'])
        display.show(Image.SQUARE_SMALL)
        sleep(500)
        display.clear()
    elif danger == 2:
        music.play(['c4'])
        display.show(Image.SQUARE)
        sleep(300)
        display.clear()
    elif danger == 3:
        music.play(['d6'])
        display.show(Image.TRIANGLE)
        sleep(100)
        display.clear()
        
def degre():
    while True:
        temp = temperature()
        if temp < 24:
            alerte(0)
        elif 24 <= temp < 26:
            alerte(1)
        elif 26 <= temp < 28:
            alerte(2)
        elif temp >= 28:
            alerte(3)
