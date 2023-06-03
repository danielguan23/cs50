import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps

#4c3083673af34c858a1a0fde83a2d6f6
#f8612638ed89463191a5699dd87beeed
def search_recipes(query):
    url = f"https://api.spoonacular.com/recipes/complexSearch?query={query}&number=6&apiKey=4c3083673af34c858a1a0fde83a2d6f6"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        recipes = []
        for result in data['results']:
            recipe_id = result['id']
            recipe_url = f"https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey=4c3083673af34c858a1a0fde83a2d6f6"
            recipe_response = requests.get(recipe_url)
            recipe_data = recipe_response.json()
            recipe = {
                'id': recipe_id,
                'title': result['title'],
                'image': result['image'],
                'sourceUrl': recipe_data['sourceUrl']
            }
            recipes.append(recipe)
        return recipes
    else:
        return None

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

