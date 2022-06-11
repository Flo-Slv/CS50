from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if not request.form.get("email"):
            return render_template(
                "apology.html",
                msg="You must enter your name !"
            )

        if not request.form.get("password"):
            return render_template(
                "apology.html",
                msg="You must enter your password !"
            )
        return "ici"
    else:
        return render_template("login.html")
