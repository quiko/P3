#  ___        __
# /\_ \    __/\ \
# \//\ \  /\_\ \ \____  _ __    __     _ __   __  __
#   \ \ \ \/\ \ \ '__`\/\`'__\/'__`\  /\`'__\/\ \/\ \
#    \_\ \_\ \ \ \ \L\ \ \ \//\ \L\.\_\ \ \/ \ \ \_\ \
#    /\____\\ \_\ \_,__/\ \_\\ \__/.\_\\ \_\  \/`____ \
#    \/____/ \/_/\/___/  \/_/ \/__/\/_/ \/_/   `/___/> \
#                                                 /\___/
#                                                 \/__/


import random

import radio


def hashing(string):
    def to_32(value):
        value = value % (2**32)
        if value >= 2**31:
            value = value - 2**32
        return int(value)

    if string:
        x = ord(string[0]) << 7
        m = 1000003
        for c in string:
            x = to_32((x * m) ^ ord(c))
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
        if char.isalpha():
            if decryption:
                modified_char = chr(
                    (ord(char.upper()) - key_as_int[key_index] + 26) % 26 + ord("A")
                )
            else:
                modified_char = chr(
                    (ord(char.upper()) + key_as_int[key_index] - 26) % 26 + ord("A")
                )
            if char.islower():
                modified_char = modified_char.lower()
            text += modified_char
        elif char.isdigit():
            if decryption:
                modified_char = str((int(char) - key_as_int[key_index]) % 10)
            else:
                modified_char = str((int(char) + key_as_int[key_index]) % 10)
            text += modified_char
        else:
            text += char
    return text


class Message:
    _key = None
    _seen_nonces = set()
    _send_counter = 0

    @classmethod
    def set_key(cls, key):
        if not key:
            raise ValueError("key must be non-empty")
        cls._key = key

    @classmethod
    def establish_connection(cls, is_child):
        if cls._key is None:
            return False
        if is_child:
            # on genere un seed et on l'envois encrypté avec la clé de base
            seed = random.randint(0, 2**30 - 1)
            Message(str(seed), 0x01).send()
            # on recois le messge de confirmation
            reply = Message.receive()
            # on check bien que c'est une réponse que l'on veux
            if reply is None or reply.type != 0x01:
                return False
            # on set le seed avec la valeur généré a la base
            random.seed(seed)
            # on génère un nouveaux nombre basé sur la seed
            c_p = random.randint(0, 2**30 - 1)
            # on check que la reponse avait le bon hash
            if reply.content != hashing(str(c_p)):
                return False
            # On modifie la key avec le nombre
            cls._key = cls._key + str(c_p)
            return True
        else:
            msg = Message.receive()
            if msg is None or msg.type != 0x01:
                return False
            try:
                seed = int(msg.content)
            except ValueError:
                return False
            random.seed(seed)
            c_p = random.randint(0, 2**30 - 1)
            Message(hashing(str(c_p)), 0x01).send()
            cls._key = cls._key + str(c_p)
            return True

    def __init__(self, content, mtype):
        self.content = content
        self.type = mtype

    def send(self):
        if Message._key is None:
            return False
        Message._send_counter += 1
        nonce = Message._send_counter
        plaintext = "{}:{}".format(nonce, self.content)  # noqa: UP032
        ciphertext = vigenere(plaintext, Message._key)
        radio.send("{}|{}|{}".format(self.type, len(plaintext), ciphertext))  # noqa: UP032
        return True

    @classmethod
    def receive(cls):
        if cls._key is None:
            return None
        packet = radio.receive()
        if packet is None:
            return None

        try:
            mtype_str, length_str, ciphertext = packet.split("|", 2)
            mtype = int(mtype_str)
            length = int(length_str)
        except (ValueError, TypeError):
            return None

        plaintext = vigenere(ciphertext, cls._key, decryption=True)

        if len(plaintext) != length or ":" not in plaintext:
            return None

        nonce, content = plaintext.split(":", 1)
        if nonce in cls._seen_nonces:
            return None
        cls._seen_nonces.add(nonce)
        return cls(content, mtype)

    @classmethod
    def reset(cls):
        """Wipe session state — simulator / unit tests only."""
        cls._key = None
        cls._password = None
        cls._seen_nonces.clear()
        cls._send_counter = 0
