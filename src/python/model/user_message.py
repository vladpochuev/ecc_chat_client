class UserMessage:
    def __init__(self,
                 from_client: str,
                 text: str):
        self.from_client = from_client
        self.text = text

    def to_dict(self):
        return {"fromClient": self.from_client,
                "text": self.text}
