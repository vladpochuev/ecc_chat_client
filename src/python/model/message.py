class Message:
    def __init__(self,
                 from_client: str,
                 to_client: str,
                 cipher_text: str,
                 nonce: str,
                 timestamp: int):
        self.from_client = from_client
        self.to_client = to_client
        self.cipher_text = cipher_text
        self.nonce = nonce
        self.timestamp = timestamp

    def to_dict(self):
        return {"fromClient": self.from_client,
                "toClient": self.to_client,
                "cipherText": self.cipher_text,
                "nonce": self.nonce,
                "timestamp": self.timestamp}
