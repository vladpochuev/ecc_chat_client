class Client:
    def __init__(self, client_id: str, public_key):
        self.clientId = client_id
        self.publicKey = public_key

    def to_dict(self):
        return {"clientId": self.clientId, "publicKey": self.publicKey}