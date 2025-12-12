import os

from flask.cli import load_dotenv

load_dotenv()

from src.python.controller import chat_controller

from flask import Flask

BASE_DIR = os.getcwd()

app = Flask(__name__,
            template_folder=os.path.join(BASE_DIR, "src", "resources", "templates"),
            static_folder=os.path.join(BASE_DIR, "src", "resources", "static"))
app.secret_key = os.getenv("SECRET_KEY")

app.register_blueprint(chat_controller)

if __name__ == "__main__":
    app.run()
