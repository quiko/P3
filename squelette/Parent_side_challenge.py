from microbit import *
import radio
import random
import music

#Can be used to filter the communication, only the ones with the same parameters will receive messages
#radio.config(group=23, channel=2, address=0x11111111)
#default : channel=7 (0-83), address = 0x75626974, group = 0 (0-255)

#Initialisation des variables du micro:bit
radio.on()
connexion_established = False
key = "KEYWORD"
connexion_key = None
nonce_list = set()
baby_state = 0
set_volume(100)

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
        #Letters encryption/decryption
        if char.isalpha():
            key_index = i % key_length
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
            key_index = i % key_length
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
    Envoi de données fournies en paramètres
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

#Unpack the packet, check the validity and return the type, length and content
def unpack_data(encrypted_packet, key):
    """
    Déballe et déchiffre les paquets reçus via l'interface radio du micro:bit
    Cette fonction renvoit les différents champs du message passé en paramètre

    :param (str) encrypted_packet: Paquet reçu
           (str) key:              Clé de chiffrement
	:return (srt)type:             Type de paquet
            (int)length:           Longueur de la donnée en caractères
            (str) message:         Données reçue
    """
    data = vigenere(encrypted_packet, key, decryption=True)
    split_data = data.split(":", 2)
    convert_length = int(split_data[1])
    return split_data[0], convert_length, split_data[2]

def receive_packet(packet_received, key):
    """
    Traite les paquets reçus via l'interface radio du micro:bit
    Cette fonction utilise la fonction unpack_data pour renvoyer les différents champs du message passé en paramètre
    Si une erreur survient, les 3 champs sont retournés vides

    :param (str) packet_received: Paquet reçue
           (str) key:              Clé de chiffrement
	:return (srt)type:             Type de paquet
            (int)lenght:           Longueur de la donnée en caractère
            (str) message:         Données reçue
    """
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
    Calcule la réponse au challenge initial de connection envoyé par l'autre micro:bit

    :param (str) challenge:            Challenge reçu
	:return (srt)challenge_response:   Réponse au challenge
    """
    challenge_response = hashing(str(challenge))
    return challenge_response

#Respond to a connexion request by sending the hash value of the number received
def respond_to_connexion_request(key):
    """
    Réponse au challenge initial de connection avec l'autre micro:bit
    Si il y a une erreur, la valeur de retour est vide

    :param (str) key:                   Clé de chiffrement
	:return (srt) challenge_response:   Réponse au challenge
    """
    # attendre un challenge
    end_time = running_time() + 10000  # 10 secondes
    while running_time() < end_time:
        packet_received = radio.receive()
        if packet_received:
           type, length, message = receive_packet(packet_received, key)
           if type == "challenge" and length == len(message):
                challenge_response = calculate_challenge_response(message)
                send_packet(key, "chal_res", challenge_response)
                return challenge_response
            
        sleep(100)  # dors un peu pour ne pas attendre trop de messages
    return ""


#result = ""
#while result == "":
    #result = respond_to_connexion_request(key)
#display.scroll(result,delay=300, loop=True)

def main():
    while True:
        pass
