import os

import requests
from flask import Blueprint
from flask import render_template, request, redirect, session, jsonify

chat_controller = Blueprint("chat", __name__)

SERVER_URL = os.getenv("SERVER_URL")

@chat_controller.route("/", methods=["GET", "POST"])
def index():
    if "username" not in session:
        if request.method == "POST":
            username = request.form.get("username")

            requests.post(f"{SERVER_URL}/register", json={"name": username})

            session["username"] = username
            return redirect("/")
        return render_template("index.html", page="register")

    users = requests.get(f"{SERVER_URL}/users").json()
    users = [u for u in users if u != session["username"]]

    return render_template("index.html", page="users", users=users)


@chat_controller.route("/chat/<name>")
def chat(name):
    return render_template("index.html", page="chat", target=name)


@chat_controller.route("/messages/<name>")
def get_messages(name):
    username = session["username"]
    r = requests.get(f"{SERVER_URL}/messages",
                     params={"from": username, "to": name})
    return jsonify(r.json())


@chat_controller.route("/send/<name>", methods=["POST"])
def send(name):
    username = session["username"]
    text = request.json["text"]

    requests.post(f"{SERVER_URL}/messages",
                  json={"from": username, "to": name, "text": text})

    return jsonify({"status": "ok"})
