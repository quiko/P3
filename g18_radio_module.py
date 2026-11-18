import radio


class Message:
    _key = None

    @classmethod
    def set_key(cls, key):
        cls._key = key

    def __init__(self, m, t) -> None:
        self.message_content = m
        self.message_type = t

    def send(self):
        packet = "{}|{}|{}".format(
            self.message_type, len(self.message_content), self.message_content
        )
        radio.send(packet)

    # def send_chalenge():
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
        except ValueError:
            return None

        return cls(content, message_type)
