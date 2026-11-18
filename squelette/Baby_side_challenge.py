from time import time

from microbit import *
import radio
import random
import music

#Can be used to filter the communication, only the ones with the same parameters will receive messages
#radio.config(group=23, channel=2, address=0x11111111)
#default : channel=7 (0-83), address = 0x75626974, group = 0 (0-255)

radio.on()
key = "KEYWORD"



def hashing(string):
	"""
	Hachage d'une chaîne de caractères fournie en paramètre.
	Le résultat est une chaîne de caractères.
	Attention : cette technique de hachage n'est pas suffisante (hachage dit cryptographique) pour une utilisation en dehors du cours.

	:param (str) string: la chaîne de caractères à hacher
	:return (str): le résultat du hachage
	"""
	def to_32(value):
		"""
		Fonction interne utilisée par hashing.
		Convertit une valeur en un entier signé de 32 bits.
		Si 'value' est un entier plus grand que 2 ** 31, il sera tronqué.

		:param (int) value: valeur du caractère transformé par la valeur de hachage de cette itération
		:return (int): entier signé de 32 bits représentant 'value'
		"""
		value = value % (2 ** 32)
		if value >= 2**31:
			value = value - 2 ** 32
		value = int(value)
		return value

	if string:
		x = ord(string[0]) << 7
		m = 1000003
		for c in string:
			x = to_32((x*m) ^ ord(c))
		x ^= len(string)
		if x == -1:
			x = -2
		return str(x)
	return ""
    
def vigenere(message, key, decryption=False):
    text = ""
    key_length = len(key)
    key_as_int = [ord(k) for k in key]

    for i, char in enumerate(str(message)):
        key_index = i % key_length
        #Letters encryption/decryption
        if char.isalpha():
            if decryption:
                modified_char = chr((ord(char.upper()) - key_as_int[key_index] + 26) % 26 + ord('A'))
            else : 
                modified_char = chr((ord(char.upper()) + key_as_int[key_index] - 26) % 26 + ord('A'))
            #Put back in lower case if it was
            if char.islower():
                modified_char = modified_char.lower()
            text += modified_char
        #Digits encryption/decryption
        elif char.isdigit():
            if decryption:
                modified_char = str((int(char) - key_as_int[key_index]) % 10)
            else:  
                modified_char = str((int(char) + key_as_int[key_index]) % 10)
            text += modified_char
        else:
            text += char
    return text
    
def send_packet(key, type, content):
    """
    Envoie de données fournie en paramètres
    Cette fonction permet de construire, de chiffrer puis d'envoyer un paquet via l'interface radio du micro:bit

    :param (str) key:       Clé de chiffrement
           (str) type:      Type du paquet à envoyer
           (str) content:   Données à envoyer
	:return none
    """
    # construire le packet 
    packet = type +":" +str(len(content))+":" + content
    
    # Chiffrer le packet 
    encrypted_packet = vigenere(packet, key)
    
    # envoyer le packet 
    radio.send(encrypted_packet)

#Decrypt and unpack the packet received and return the fields value
def unpack_data(encrypted_packet, key):
    """
    Déballe et déchiffre les paquets reçus via l'interface radio du micro:bit
    Cette fonction renvoit les différents champs du message passé en paramètre

    :param (str) encrypted_packet: Paquet reçu
           (str) key:              Clé de chiffrement
	:return (srt)type:             Type de paquet
            (int)lenght:           Longueur de la donnée en caractères
            (str) message:         Données reçues
    """
    # Décripter le paquet reçu 
    decrypt = vigenere(encrypted_packet, key, decryption=True)
    
    # diviser en 3 parties le paquet décrypté et retourner les valeurs
    split_decrypt = decrypt.split(":", 2)
    convert_length = int(split_decrypt[1])
    return split_decrypt[0], convert_length, split_decrypt[2]


#Unpack the packet, check the validity and return the type, length and content
def receive_packet(packet_received, key):
    """
    Traite les paquets reçue via l'interface radio du micro:bit
    Cette fonction permet de construire, de chiffrer puis d'envoyer un paquet via l'interface radio du micro:bit
    Si une erreur survient, les 3 champs sont retournés vides

    :param (str) packet_received: Paquet reçue
           (str) key:              Clé de chiffrement
	:return (srt)type:             Type de paquet
            (int)lenght:           Longueur de la donnée en caractère
            (str) message:         Données reçue
    """
    # si le paquet reçu est vide, on retourne des valeurs vides
    if packet_received == "" or packet_received == None:
            return "", 0, ""
    try:
    # deballer le paquet reçu avec unpack_data 
        type, length, message = unpack_data(packet_received, key)
            
    except: 
        # retourner des valeurs vides si une erreur survient
        return "", 0, ""
            
    # si legnth du message ne correspond pas à la longueur indiquée, on retourne des valeurs vides
    if length != len(message):
        return "", 0, ""
    # Sinon , on retourne les valeurs du paquet
    return type, length, message
    
#Calculate the challenge response
def calculate_challenge_response(challenge):
    """
    Calcule la réponse au challenge initial de connection avec l'autre micro:bit

    :param (str) challenge:            Challenge reçu
	:return (srt)challenge_response:   Réponse au challenge
    """
    challenge_response = hashing(str(challenge))
    return challenge_response
    
#Ask for a new connection with a micro:bit of the same group
def establish_connexion(key):
    """
    Etablissement de la connexion avec l'autre micro:bit
    Si il y a une erreur, la valeur de retour est vide

    :param (str) key:                  Clé de chiffrement
	:return (srt)challenge_response:   Réponse au challenge
    """
    # Générer un nombre random coverti en string pour le challenge
    challenge = str(random.randint(0, 1000000))
    # l'envoyer avec send_packet
    send_packet(key, "challenge",challenge)
    
    end_time = time.ticks_ms() + 5000  # 5 seconds timeout
    while time.ticks_ms() < end_time:
        packet_received = radio.receive()
        expected_response = calculate_challenge_response(challenge)
        if packet_received:
            type, length, message = receive_packet(packet_received, key)
            if type == "chal_res" and message == expected_response:
                return message
                
        sleep(100)  # dors un peu pour ne pas attendre trop de messages
    
    return ""  # Return un string vide si le timeout est atteint sans recevoir de réponse

#encrypted = vigenere("state:1:1", key)
#print(unpack_data(encrypted, key)) 
#display.scroll("[" + establish_connexion(key) + "]",delay=300, loop=True)

def main():
    return True