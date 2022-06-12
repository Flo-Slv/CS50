from flask import Flask, render_template, request, flash, redirect
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

db = sqlite3.connect("cs.db", check_same_thread=False)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if not email:
            return render_template(
                "apology.html",
                msg="You must enter your email !"
            )

        if not password:
            return render_template(
                "apology.html",
                msg="You must enter your password !"
            )
        flash("Done !")
        return render_template("profile.html")
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        password = request.form.get("password")
        hash = generate_password_hash(request.form.get("password"))
        confirmation = request.form.get("confirmation")
        email = request.form.get("email")
        name = request.form.get("name")

        if not email:
            return render_template("apology.html", msg="You must enter your email !")

        if not password:
            return render_template("apology.html", msg="You must enter your password !")

        if not confirmation:
            return render_template("apology.html", msg="You must confirm your password !")

        if password != confirmation:
            return render_template("apology.html", msg="Both passswords should be identical !")

        if not name:
            return render_template("apology.html", msg="You must enter your name !")

        rows = db.execute("SELECT * FROM users WHERE email=?;", (email,))
        res = rows.fetchall()

        if len(res) == 1:
            return render_template("apology.html", msg="Sorry, this email already have an account !")

        db.execute("INSERT INTO users(email, password, name) VALUES(?, ?, ?);",
                (email, hash, name))

        db.commit()

        # flash("Congratulations ! You were successfully registered ! You can now login.")

        return redirect("/")

        return "TO DO !"
    else:
        return render_template("register.html")
