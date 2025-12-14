import os
import sys

from dotenv import load_dotenv
from flask import Flask

load_dotenv()

def resource_path(relative_path) -> str:
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

app = Flask(
    __name__,
    template_folder=resource_path("src/resources/templates"),
    static_folder=resource_path("src/resources/static")
)

from src.python.controller.chat_controller import chat_controller
app.register_blueprint(chat_controller)

if __name__ == "__main__":
    app.run(port=os.getenv("FLASK_RUN_PORT"))
