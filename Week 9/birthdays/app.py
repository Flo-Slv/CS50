import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        # TODO: Add the user's entry into the database
        if not request.form.get("name"):
            return render_template("apology.html", msg="You need to add your name !")

        if not request.form.get("day"):
            return render_template("apology.html", msg="You need to add your birthday day !")

        if not request.form.get("month"):
            return render_template("apology.html", msg="You need to add your birthday month !")

        db.execute("INSERT INTO birthdays(name, day, month) VALUES(?, ?, ?)",
                   request.form.get("name"), request.form.get("day"), request.form.get("month"))

        # flash("Birthday successfully added !")

        return redirect("/")

    else:

        # TODO: Display the entries in the database on index.html
        data = db.execute("SELECT * FROM birthdays")
        return render_template("index.html", data=data)


@app.route("/delete", methods=["POST"])
def delete():
    if request.method == "POST":
        if not request.form.get("id"):
            return render_template("apology.html", msg="You need to have an id to delete!")

        db.execute("DELETE FROM birthdays WHERE id=?", request.form.get("id"))

        return redirect("/")
