import os
import traceback
from datetime import datetime

import requests
from flask import Blueprint
from flask import render_template, request, redirect, session, jsonify

from src.python.model import Client, Message, UserMessage
from src.python.model.encrypted_text import EncryptedText
from src.python.service import public_key_pem as public_key, get_encrypted_text, get_decrypted_text

chat_controller = Blueprint("chat", __name__)

SERVER_URL = os.getenv("SERVER_URL")

clients = {}


@chat_controller.route("/", methods=["GET", "POST"])
def index():
    global clients
    if "username" not in session:
        if request.method == "POST":
            username = request.form.get("username")

            requests.post(f"{SERVER_URL}/register", json=Client(username, public_key).to_dict())

            session["username"] = username
            return redirect("/")
        return render_template("index.html", page="register")

    received_clients = requests.get(f"{SERVER_URL}/clients").json()
    valid_clients = [Client(u["clientId"], u["publicKey"]) for u in received_clients if
                     u["clientId"] != session["username"]]
    usernames = [client.client_id for client in valid_clients]

    for valid_client in valid_clients:
        clients[valid_client.client_id] = valid_client

    return render_template("index.html", page="users", users=usernames)


@chat_controller.route("/chat/<name>")
def chat(name):
    return render_template("index.html", page="chat", target=name)


@chat_controller.route("/messages/<name>")
def get_messages(name):
    global clients

    username = session["username"]
    r = requests.get(f"{SERVER_URL}/messages/history",
                     params={"from": username, "to": name})
    user_messages = []
    for message in r.json():
        try:
            message = Message(message["fromClient"], message["toClient"], message["cipherText"], message["nonce"],
                              message["timestamp"])
            encrypted_text = EncryptedText(message.cipher_text, message.nonce)

            if message.to_client == username:
                user_public_key = clients[message.from_client].public_key
            else:
                user_public_key = clients[message.to_client].public_key

            text = get_decrypted_text(encrypted_text, user_public_key)
            user_messages.append(UserMessage(message.from_client, text))
        except Exception:
            print("Error while decrypting the message")
            traceback.print_exc()
    return jsonify([m.to_dict() for m in user_messages])


@chat_controller.route("/send/<name>", methods=["POST"])
def send(name):
    global clients

    from_client = session["username"]
    text = request.json["text"]
    encrypted_text = get_encrypted_text(text, clients[name].public_key)
    timestamp = datetime.now().timestamp()

    message = Message(from_client, name, encrypted_text.cipher_text, encrypted_text.nonce, int(timestamp))

    requests.post(f"{SERVER_URL}/messages/send",
                  json=message.to_dict())

    return jsonify({"status": "ok"})
