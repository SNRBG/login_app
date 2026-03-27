from flask import Flask, render_template, request, redirect, session
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
app.secret_key = "secretkey"

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["userDB"]
users = db["users"]

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = users.find_one({"username": username})

        if user and bcrypt.checkpw(password.encode('utf-8'), user["password"]):
            session["user"] = username
            return redirect("/dashboard")
        else:
            return "Invalid credentials"

    return render_template("login.html")


@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password = request.form["password"]

    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    users.insert_one({
        "username": username,
        "password": hashed_pw
    })

    return redirect("/")


@app.route("/dashboard")
def dashboard():
    if "user" in session:
        return render_template("dashboard.html", user=session["user"])
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
