from flask import Flask, render_template, request, redirect, url_for, session, flash
from playwright.sync_api import sync_playwright
import json

app = Flask(__name__)
app.secret_key = "secret_key_123"

# User credentials file
USER_DATA_FILE = "user_data.json"

def load_user_data():
    try:
        with open(USER_DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_user_data(data):
    with open(USER_DATA_FILE, "w") as file:
        json.dump(data, file)

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_data = load_user_data()
        if username in user_data and user_data[username] == password:
            session["user"] = username
            return redirect(url_for("search"))
        else:
            flash("Invalid credentials. Please try again.")
    return render_template("index.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_data = load_user_data()
        if username in user_data:
            flash("Username already exists. Please choose another one.")
        else:
            user_data[username] = password
            save_user_data(user_data)
            flash("Sign-up successful! Please log in.")
            return redirect(url_for("login"))

    return render_template("signup.html")

@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        username = request.form["username"]

        user_data = load_user_data()
        if username in user_data:
            flash(f"Your password is: {user_data[username]}")
        else:
            flash("Username not found.")

    return render_template("forgot_password.html")

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
            # Use Playwright to fetch the dynamic content
            with sync_playwright() as p:
                browser = p.firefox.launch(headless=True)
                page = browser.new_page()
                page.goto(url, timeout=60000)  # Load page with a timeout
                rendered_html = page.content().lower()
                browser.close()

            keyword_lower = keyword.lower()

            # Check if the keyword exists in the rendered HTML
            flagged = keyword_lower in rendered_html
            return render_template("result.html", flagged=flagged, url=url, keyword=keyword)

        except Exception as e:
            flash(f"Error fetching the URL: {str(e)}")
            return redirect(url_for("search"))

    return render_template("search.html")

if __name__ == "__main__":
    app.run(debug=True)
