import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, search_recipes

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///recipe.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
        userrecipes = db.execute("SELECT recipename, recipe, recipeid FROM recipes WHERE userid = ?", session["user_id"])
        savedrecipes = db.execute("SELECT image, name, link FROM saved WHERE userid = ?", session["user_id"])
        saved = db.execute('SELECT link FROM saved WHERE saved.userid = ?', session["user_id"])
        saved_links = [row['link'] for row in saved]
        # Convert userrecipes to a list
        userrec = [{"recipename": row["recipename"], "recipe": row["recipe"], "recipeid": row["recipeid"]} for row in userrecipes]
        # Convert savedrecipes to a list
        savedrec = [{"image": row["image"], "name": row["name"], "link": row["link"]} for row in savedrecipes]
        return render_template("index.html", userrec=userrec, savedrec=savedrec, saved_links=saved_links)

@app.route('/delete', methods=["POST"])
@login_required
def delete():
    recipeid = request.form['recipeid']
    if recipeid:
        db.execute('DELETE FROM recipes WHERE userid = ? AND recipeid = ?', session["user_id"], recipeid)
    return redirect("/")

@app.route("/expanded_text/<string:recipename>/<string:recipe>")
@login_required
def expanded_text(recipename, recipe):
    # Render the expanded text view with the recipename and recipe as parameters
    return render_template("expanded_text.html", recipename=recipename, recipe=recipe)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        username = request.form.get("username")
        password = request.form.get("password")
        if not username:
            username_error = "Please provide a username"
            return render_template("login.html", username_error=username_error, username=username, password=password)

        # Ensure password was submitted
        elif not password:
            password_error = "Please provide a password"
            return render_template("login.html", password_error=password_error, username=username, password=password)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            username_error = "Invalid username and/or password"
            return render_template("login.html", username_error=username_error, username=username, password=password)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html", username=None, password=None)


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        rows = db.execute("SELECT username FROM users WHERE username = ?", username)
        # Ensure username was submitted
        if not username:
            username_error = "Please provide a username"
            return render_template("register.html", username_error=username_error, username=username, password=password, confirmation=confirmation)

        if len(rows) > 0:
            username_error = "Username exists"
            return render_template("register.html", username_error=username_error, username=username, password=password, confirmation=confirmation)

        # Ensure password was submitted
        elif not password:
            password_error = "Please provide a password"
            return render_template("register.html", password_error=password_error, username=username, password=password, confirmation=confirmation)

        elif not confirmation:
            confirm_error = "Please provide password again"
            return render_template("register.html", confirm_error=confirm_error, username=username, password=password, confirmation=confirmation)

        elif not password == confirmation:
            confirm_error = "Password does not match"
            return render_template("register.html", confirm_error=confirm_error, username=username, password=password, confirmation=confirmation)

        else:
            hash = generate_password_hash(
                password, method='pbkdf2:sha256', salt_length=8
            )

            db.execute(
                "INSERT INTO users (username, hash) VALUES (?, ?)", username, hash
            )

        # Redirect user to home page
        return redirect("/login")


        # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html", username=None, password=None, confirmation=None)



@app.route('/discover', methods=['GET', 'POST'])
@login_required
def discover():
    saved = db.execute('SELECT link FROM saved WHERE saved.userid = ?', session["user_id"])
    saved_links = [row['link'] for row in saved]

    if request.method == 'POST':
        query = request.form['query']
        session['query'] = query
    else:
        query = session.get('query', '')

    if query:
        recipes = search_recipes(query)  # Placeholder for actual search function
        return render_template('discover.html', recipes=recipes, saved_links=saved_links, query=query)
    else:
        return render_template('discover.html', saved_links=saved_links)


@app.route('/save', methods=["POST"])
@login_required
def save():
    image = request.form['recipe_image']
    name = request.form['recipe_name']
    link = request.form['recipe_source']
    saved = db.execute('SELECT link FROM saved WHERE saved.userid = ?', session["user_id"])
    saved_links = [row['link'] for row in saved]
    if link in saved_links:
        db.execute('DELETE FROM saved WHERE userid = ? AND link = ?', session["user_id"], link )
    else:
        db.execute(
        'INSERT INTO saved (userid, image, name, link) VALUES (?, ?, ?, ?)', session["user_id"], image, name, link
        )
    return redirect("/discover")




@app.route('/saveindex', methods=["POST"])
@login_required
def saveindex():
    image = request.form['recipe_image']
    name = request.form['recipe_name']
    link = request.form['recipe_source']
    saved = db.execute('SELECT link FROM saved WHERE saved.userid = ?', session["user_id"])

    saved_links = [row['link'] for row in saved]

    if link in saved_links:
        db.execute('DELETE FROM saved WHERE userid = ? AND link = ?', session["user_id"], link )
    else:
        db.execute(
        'INSERT INTO saved (userid, image, name, link) VALUES (?, ?, ?, ?)', session["user_id"], image, name, link
        )
    return redirect("/")



@app.route('/add', methods=["GET", "POST"])
@login_required
def add():

    if request.method == "POST":
        userrecipes = db.execute("SELECT recipename, recipe, recipeid FROM recipes WHERE userid = ?", session["user_id"])
        savedrecipes = db.execute("SELECT image, name, link FROM saved WHERE userid = ?", session["user_id"])
        saved = db.execute('SELECT link FROM saved WHERE saved.userid = ?', session["user_id"])
        saved_links = [row['link'] for row in saved]
        # Convert userrecipes to a list
        userrec = [{"recipename": row["recipename"], "recipe": row["recipe"], "recipeid": row["recipeid"]} for row in userrecipes]
        # Convert savedrecipes to a list
        savedrec = [{"image": row["image"], "name": row["name"], "link": row["link"]} for row in savedrecipes]

        recipename = request.form.get('recipename')
        recipe = request.form.get('recipe')
        if not recipename:
            error = "Please provide a name."
            return render_template("index.html", error=error, userrec=userrec, savedrec=savedrec, saved_links=saved_links)
        if not recipe:
            error = "Please provide instructions."
            return render_template("index.html", error=error, userrec=userrec, savedrec=savedrec, saved_links=saved_links)
        else:
            db.execute("INSERT INTO recipes (userid, recipename, recipe) VALUES (?, ?, ?)", session["user_id"], recipename, recipe)
            return redirect("/")
    else:
        return redirect("/")


@app.route('/social', methods=["GET", "POST"])
@login_required
def social():
    if request.method == "POST":
        userrecipes = db.execute("SELECT recipename, recipe, recipeid, likes FROM recipes ORDER BY likes DESC LIMIT 9")
        userrec = [{"recipename": row["recipename"], "recipe": row["recipe"], "recipeid": row["recipeid"], "likes":row["likes"]} for row in userrecipes]
        userliked = db.execute("SELECT recipeid FROM 'like' WHERE userid = ?", session["user_id"])
        userlikelist = [row["recipeid"] for row in userliked]
        formrecipeid = request.form["recipeid"]
        formrecipeid = int(formrecipeid)

        newrecipes = db.execute("SELECT recipename, recipe, recipeid, likes FROM recipes ORDER BY date, datetime DESC LIMIT 9")
        newrec = [{"recipename": row["recipename"], "recipe": row["recipe"], "recipeid": row["recipeid"], "likes":row["likes"]} for row in newrecipes]

        if formrecipeid in userlikelist:
            db.execute("DELETE FROM 'like' WHERE userid = ? AND recipeid = ?", session["user_id"], formrecipeid)
            db.execute("UPDATE 'recipes' SET likes = likes - 1 WHERE recipeid = ?", formrecipeid)
        else:
            db.execute("INSERT INTO 'like' (userid, recipeid) VALUES (?, ?)", session["user_id"], formrecipeid)
            db.execute("UPDATE 'recipes' SET likes = likes + 1 WHERE recipeid = ?", formrecipeid)

        userrecipes = db.execute("SELECT recipename, recipe, recipeid, likes FROM recipes ORDER BY likes DESC LIMIT 9")
        userrec = [{"recipename": row["recipename"], "recipe": row["recipe"], "recipeid": row["recipeid"], "likes":row["likes"]} for row in userrecipes]
        userliked = db.execute("SELECT recipeid FROM 'like' WHERE userid = ?", session["user_id"])
        userlikelist = [row["recipeid"] for row in userliked]
        formrecipeid = request.form["recipeid"]

        newrecipes = db.execute("SELECT recipename, recipe, recipeid, likes FROM recipes ORDER BY date, datetime DESC LIMIT 9")
        newrec = [{"recipename": row["recipename"], "recipe": row["recipe"], "recipeid": row["recipeid"], "likes":row["likes"]} for row in newrecipes]

        return render_template("social.html", userrec=userrec, userlikelist=userlikelist, newrec=newrec)
    else:
        userrecipes = db.execute("SELECT recipename, recipe, recipeid, likes FROM recipes ORDER BY likes DESC LIMIT 9")
        userrec = [{"recipename": row["recipename"], "recipe": row["recipe"], "recipeid": row["recipeid"], "likes":row["likes"]} for row in userrecipes]
        userliked = db.execute("SELECT recipeid FROM 'like' WHERE userid = ?", session["user_id"])
        userlikelist = [row["recipeid"] for row in userliked]

        newrecipes = db.execute("SELECT recipename, recipe, recipeid, likes FROM recipes ORDER BY date, datetime DESC LIMIT 9")
        newrec = [{"recipename": row["recipename"], "recipe": row["recipe"], "recipeid": row["recipeid"], "likes":row["likes"]} for row in newrecipes]

        return render_template("social.html", userrec=userrec, userlikelist=userlikelist, newrec=newrec)