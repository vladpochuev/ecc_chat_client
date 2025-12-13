class Client:
    def __init__(self, client_id: str, public_key):
        self.client_id = client_id
        self.public_key = public_key

    def to_dict(self):
        return {"clientId": self.client_id, "publicKey": self.public_key}