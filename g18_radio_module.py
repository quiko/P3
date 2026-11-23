import radio
import random


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
        value = value % (2**32)
        if value >= 2**31:
            value = value - 2**32
        value = int(value)
        return value

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


class Message:
    _key = None
    _nonce = []

    @classmethod
    def set_key(cls, key):
        cls._key = key

    def __init__(self, m, t) -> None:
        self.message_content = m
        self.message_type = t

    def send(self):
        nonce = random.randint(000, 999)

        packet = "{}|{}|{}:{}".format(  # noqa: UP032
            self.message_type,
            len(self.message_content) + len(str(nonce)),
            nonce,
            self.message_content,
        )
        radio.send(packet)
        h = hashing(packet)
        while Message.receive() != (0x02, h):
            radio.send(packet)

    def send_raw(self):
        nonce = random.randint(000, 999)

        packet = "{}|{}|{}:{}".format(  # noqa: UP032
            self.message_type,
            len(self.message_content) + len(str(nonce)),
            nonce,
            self.message_content,
        )
        radio.send(packet)

    def send_chalenge(self, cls):
        seed = random.randint(00000, 99999)
        random.seed(seed)
        Message(seed, 0x01).send()
        h = hashing(random.randint(0000, 1111))
        chalenge_response = cls.receive_raw()
        return chalenge_response == (h, 1)

    @classmethod
    def receive(cls):
        key = cls._key
        if key is None:
            return None

        packet = radio.receive()

        if packet is None:
            return None

        try:
            message_type, length, content = packet.split("|", 2)
            packet_nonce, message = content.split(":")
            message_type = int(message_type)
        except ValueError:
            return None

        if packet_nonce in cls._nonce:
            return None
        else:
            cls._nonce.append(packet_nonce)
            confirmation_message = cls(hashing(message), message_type)
            confirmation_message.send_raw()

        return cls(message, message_type)

    @classmethod
    def receive_raw(cls):
        key = cls._key
        if key is None:
            return None

        packet = radio.receive()

        if packet is None:
            return None

        try:
            message_type, length, content = packet.split("|", 2)
            packet_nonce, message = content.split(":")
            message_type = int(message_type)
        except ValueError:
            return None

        if packet_nonce in cls._nonce:
            return None
        else:
            cls._nonce.append(packet_nonce)

        return cls(message, message_type)
