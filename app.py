from flask import Flask, render_template, request, redirect, url_for, session, flash
import requests

app = Flask(__name__)
app.secret_key = "secret_key_123"

# User credentials
USER_CREDENTIALS = {"admin": "password"}

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            session["user"] = username
            return redirect(url_for("search"))
        else:
            flash("Invalid credentials. Please try again.")
    return render_template("index.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

@app.route("/search", methods=["GET", "POST"])
def search():
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        url = request.form["url"]
        keyword = request.form["keyword"]

        try:
            response = requests.get(url)
            if keyword.lower() in response.text.lower():
                return render_template("result.html", flagged=True, url=url, keyword=keyword)
            else:
                return render_template("result.html", flagged=False, url=url, keyword=keyword)
        except Exception as e:
            flash(f"Error fetching the URL: {str(e)}")
            return redirect(url_for("search"))

    return render_template("search.html")

if __name__ == "__main__":
    app.run(debug=True)
