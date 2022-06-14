from flask import Flask, render_template, request, flash, redirect, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3

from helpers import apology, login_required

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Connexion to database
db = sqlite3.connect("cs.db", check_same_thread=False)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Forget any user_id
        session.clear()

        email = request.form.get("email")
        password = request.form.get("password")

        if not email:
            return apology("You must enter your email", 403)

        if not password:
            return apology("You must enter your password", 403)

        rows = db.execute("SELECT * FROM users WHERE email=?", (email,))
        res = rows.fetchall()

        print(res)

        if len(res) != 1 or not check_password_hash(res[0][2], password):
            return apology("Invalid email or password", 403)

        # Remember which user has logged in
        session["user_id"] = res[0][0]

        # Redirect user to home page
        return redirect("/")
    else:
        return render_template("login.html")


@app.route("/")
@login_required
def index():
    return render_template("profile.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        password = request.form.get("password")
        hash = generate_password_hash(request.form.get("password"))
        confirmation = request.form.get("confirmation")
        email = request.form.get("email")
        name = request.form.get("name")

        if not email:
            return apology("You must enter your email", 403)

        if not password:
            return apology("You must enter your password", 403)

        if not confirmation:
            return apology("You must enter your confirmation password", 403)

        if password != confirmation:
            return apology("Both password should be identical !", 403)

        if not name:
            return apology("You must enter your name", 403)

        rows = db.execute("SELECT * FROM users WHERE email=?;", (email,))
        res = rows.fetchall()

        if len(res) == 1:
            return apology("Sorry, this email have already an account", 403)

        db.execute("INSERT INTO users(email, password, name) VALUES(?, ?, ?);",
                (email, hash, name))

        db.commit()

        # flash("Congratulations ! You were successfully registered ! You can now login.")

        return redirect("/")

        return "TO DO !"
    else:
        return render_template("register.html")
