import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    # select values from db about user's portfolio
    rows = db.execute("SELECT symbol, name, shares FROM stocks WHERE user_id=? ORDER BY symbol", session["user_id"])

    # lookup current price for each stock and calculate total value of each stock
    # add the information to rows to display on website
    stock_total = 0
    for row in rows:
        current_price = lookup(row["symbol"])["price"]
        total = current_price*int(row["shares"])
        row["current_price"] = usd(current_price)
        row["total"] = usd(total)
        stock_total += total

    # query table users for current cash available
    user_cash = db.execute("SELECT cash FROM users WHERE id=?", session["user_id"])[0]["cash"]

    total = user_cash + stock_total

    return render_template("index.html", rows=rows, user_cash=usd(user_cash), total=usd(total))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("must provide a symbol", 400)

        if not request.form.get("shares"):
            return apology("must provide a number of shares", 400)

        if not request.form.get("shares").isdigit():
            return apology("must provide a valid numeric positiv number", 400)

        if int(request.form.get("shares")) <= 0:
            return apology("shares should be positive", 400)

        quote = lookup(request.form.get("symbol"))

        if not quote:
            return apology("invalid symbol")

        unit_price = quote["price"]

        total = unit_price * int(request.form.get("shares"))

        user_cash = db.execute("SELECT cash FROM users WHERE id=?", session["user_id"])

        if user_cash[0]["cash"] < total:
            return apology("not enough money to buy !")
        else:
            date = datetime.datetime.now()

            # update user's history
            db.execute("UPDATE users SET cash=? WHERE id=?", user_cash[0]["cash"]-total, session["user_id"])

            db.execute("INSERT INTO history(user_id, symbol, name, shares, unit_price, total_price, date) VALUES(?, ?, ?, ?, ?, ?, ?)",
                       session["user_id"], request.form.get("symbol").upper(), quote["name"], int(request.form.get("shares")), unit_price, total, date)

            # check if the stock in user's portfolio
            instock = db.execute("SELECT symbol FROM stocks WHERE user_id=? AND symbol=?",
                                 session["user_id"], request.form.get("symbol").upper())

            name = quote["name"]

            if not instock:
                db.execute("INSERT INTO stocks(user_id, symbol, name, shares) VALUES(?, ?, ?, ?)",
                           session["user_id"], request.form.get("symbol").upper(), name, int(request.form.get("shares")))

            else:
                rows = db.execute("SELECT shares FROM stocks WHERE user_id=? and symbol=?",
                                  session["user_id"], request.form.get("symbol").upper())

                db.execute("UPDATE stocks SET shares=? WHERE user_id=? and symbol=?",
                           int(rows[0]["shares"]) + int(request.form.get("shares")), session["user_id"], request.form.get("symbol").upper())

            user_cash = db.execute("SELECT cash FROM users WHERE id=?", session["user_id"])

            flash("Congratulations ! Transaction is successful !")

            return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    # select values from db about user's transactions
    rows = db.execute("SELECT symbol, name, shares, unit_price, total_price, date FROM history WHERE user_id=?", session["user_id"])

    for row in rows:
        row["unit_price"] = usd(row["unit_price"])
        row["total_price"] = usd(row["total_price"])

    return render_template("history.html", rows=rows)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "POST":
        if not request.form.get("old_password"):
            return apology("must provide old password", 403)

        if not request.form.get("password"):
            return apology("must provide a new password", 403)

        if not request.form.get("confirmation"):
            return apology("must provide a confirmation password", 403)

        if request.form.get("password") != request.form.get("confirmation"):
            return apology("both new password should be identical", 403)

        if request.form.get("old_password") == request.form.get("password"):
            return apology("New password should be different than old one")

        rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])

        if not check_password_hash(rows[0]["hash"], request.form.get("old_password")):
            return apology("Old password is not correct", 403)

        hash_password = generate_password_hash(request.form.get("password"))

        db.execute("UPDATE users SET hash=? WHERE id=?", hash_password, session["user_id"])

        flash("Congratulations ! Password has been successfully changed !")

        # redirect user to home page
        return redirect("/")
    else:
        return render_template("change_password.html")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("must provide a symbol", 400)
        else:
            quote = lookup(request.form.get("symbol"))

            if not quote:
                return apology("Invalid symbol", 400)
            else:
                return render_template("quoted.html", quote=quote, price=usd(quote["price"]))
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # forget any user_id
    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 400)

        if not request.form.get("password"):
            return apology("must provide password", 400)

        if not request.form.get("confirmation"):
            return apology("must provide a confirmation for the password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        if len(rows) == 1:
            return apology("Username already exist, please choose an other one !")

        if request.form.get("password") != request.form.get("confirmation"):
            return apology("both passwords should be identical", 400)

        password_hash = generate_password_hash(request.form.get("password"))

        db.execute("INSERT INTO users(username, hash) VALUES(?, ?)", request.form.get("username"), password_hash)

        flash("Congratulations ! You were successfully registered ! You can now login.")

        return render_template("login.html")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("must provide a symbol", 403)

        if not request.form.get("shares"):
            return apology("must provide a number of shares", 403)

        if not request.form.get("shares").isdigit():
            return apology("must provide a valid numeric positiv number", 400)

        if int(request.form.get("shares")) <= 0:
            return apology("shares should be positive", 403)

        quote = lookup(request.form.get("symbol"))

        if not quote:
            return apology("invalid symbol")

        # query database to check if user has shares of the stock
        rows = db.execute("SELECT shares FROM stocks WHERE user_id=? AND symbol=?",
                          session["user_id"], request.form.get("symbol").upper())

        # check if user have enough shares of the stock to sell
        if not rows or int(request.form.get("shares")) > int(rows[0]["shares"]):
            return apology("don't have enough shares to sell")
        else:
            # delete stock from user's portfolio if user sold all shares of the stock
            if int(rows[0]["shares"]) == int(request.form.get("shares")):
                db.execute("DELETE FROM stocks WHERE user_id=? and symbol=?",
                           session["user_id"], request.form.get("symbol").upper())

            # update user's portfolio after selling
            db.execute("UPDATE stocks SET shares=? WHERE user_id=? AND symbol=?",
                       int(rows[0]["shares"])-int(request.form.get("shares")), session["user_id"], request.form.get("symbol").upper())

            flash("Sold ! Transaction is succesfull !")

            # calculate total price of the shares to sell
            unit_price = quote["price"]
            total_value = unit_price*int(request.form.get("shares"))

            date = datetime.datetime.now()
            name = quote["name"]

            # update user's history
            db.execute("INSERT INTO history(user_id, symbol, name, shares, unit_price, total_price, date) VALUES(?, ?, ?, ?, ?, ?, ?)",
                       session["user_id"], request.form.get("symbol").upper(), name, "-" + request.form.get("shares"), unit_price, total_value, date)

            # update cash in users table for the user
            rows = db.execute("SELECT cash FROM users WHERE id=?", session["user_id"])
            db.execute("UPDATE users SET cash=? WHERE id=?", rows[0]["cash"] + total_value, session["user_id"])

            return redirect("/")
    else:
        rows = db.execute("SELECT * FROM stocks WHERE user_id=?", session["user_id"])
        return render_template("sell.html", rows=rows)
