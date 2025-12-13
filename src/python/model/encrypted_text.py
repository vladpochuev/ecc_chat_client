class EncryptedText:
    def __init__(self, cipher_text: str, nonce: str):
        self.cipher_text = cipher_text
        self.nonce = nonce