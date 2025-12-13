class Message:
    def __init__(self,
                 from_client: str,
                 to_client: str,
                 cipher_text: str,
                 nonce: str,
                 timestamp: int):
        self.fromClient = from_client
        self.toClient = to_client
        self.cipher_text = cipher_text
        self.nonce = nonce
        self.timestamp = timestamp

    def to_dict(self):
        return {"fromClient": self.fromClient,
                "toClient": self.toClient,
                "cipherText": self.cipher_text,
                "nonce": self.nonce,
                "timestamp": self.timestamp}
