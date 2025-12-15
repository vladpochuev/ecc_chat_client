import os
import sys

import webview
from dotenv import load_dotenv
from flask import Flask

load_dotenv()


def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

app = Flask(
    __name__,
    template_folder=resource_path("src/resources/templates")
)

app.secret_key = os.getenv("SECRET_KEY")

window = webview.create_window('Chat', app)

from src.python.controller.chat_controller import chat_controller

app.register_blueprint(chat_controller)

if __name__ == "__main__":
    webview.start()
