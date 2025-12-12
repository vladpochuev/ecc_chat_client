import os

import requests
from flask import Flask, render_template, request, redirect, session, jsonify
from flask.cli import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
SERVER_URL = os.getenv("SERVER_URL")

@app.route("/", methods=["GET", "POST"])
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


@app.route("/chat/<name>")
def chat(name):
    return render_template("index.html", page="chat", target=name)


@app.route("/messages/<name>")
def get_messages(name):
    username = session["username"]
    r = requests.get(f"{SERVER_URL}/messages",
                     params={"from": username, "to": name})
    return jsonify(r.json())


@app.route("/send/<name>", methods=["POST"])
def send(name):
    username = session["username"]
    text = request.json["text"]

    requests.post(f"{SERVER_URL}/messages",
                  json={"from": username, "to": name, "text": text})

    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run()
