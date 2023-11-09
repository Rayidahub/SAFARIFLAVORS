from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv, find_dotenv 
from flask_mongoengine import MongoEngine
from mongoengine import connect, Document, StringField, ReferenceField, ListField
from flask_admin import Admin
from flask_admin.contrib.mongoengine import ModelView
from models.schema import Region, SubRegion, Country, Recipe
from models.user import User
from models.model import Food
import os
import requests
from urllib.parse import unquote
load_dotenv(find_dotenv('safari.env'))


app = Flask(__name__)
# app.config['MONGODB_SETTINGS'] = {
#     'db': 'recipe_db',
#     'host': 'mongodb://localhost:27017/recipe_db'   
# }

# Set up the configuration for your API key from https://spoonacular.com/food-api
API_KEY = os.getenv('API')

# Initialize the MongoEngine
#db = MongoEngine(app)

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure secret key

# Configure the uploads folder
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'static')
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg', 'png', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Implement search through third party api
def search_recipes(query):
    url = f'https://api.spoonacular.com/recipes/complexSearch'
    params = {
        'apiKey': API_KEY,
        'query': query,
        'number': 10,
        'instructionsRequired': True,
        'addRecipeInformation': True,
        'fillIngredients': True,
    }

    # Send a GET request to the Spoonacular API with the query parameters
    response = requests.get(url, params=params)
    # If the API call is successful
    if response.status_code == 200:
        # Parse the API response as JSON data
        data = response.json()
        # Return the list of recipe results
        return data['results']
    # If the API call is not successful
    return []

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def display_recipes():
    if request.method == 'POST':
        # If a form is submitted
        query = request.form.get('search_query', '')
        # Perform a search for recipes with the given query
        recipes = search_recipes(query)
        print(recipes)
        # Render the main page with the search results and the search query
        return render_template('home.html', recipes=recipes, search_query=query)
    
    # If it's a GET request or no form submitted
    search_query = request.args.get('search_query', '')
    decoded_search_query = unquote(search_query)
    # Perform a search for recipes with the decoded search query
    recipes = search_recipes(decoded_search_query)
    # Render the main page
    return render_template('home.html', recipes=recipes, search_query=decoded_search_query)

# Route to view a specific recipe with a given recipe ID
@app.route('/recipe/<int:recipe_id>')
def view_recipe(recipe_id):
    # Get the search query from the URL query parameters
    search_query = request.args.get('search_query', '')
    # Build the URL to get information about the specific recipe ID from Spoonacular API
    url = f'https://api.spoonacular.com/recipes/{recipe_id}/information'
    params = {
        'apiKey': API_KEY,
    }

    # Send a GET request to the Spoonacular API to get the recipe information
    response = requests.get(url, params=params)
    # If the API call is successful
    if response.status_code == 200:
        recipe = response.json()
        return render_template('recipe.html', recipe=recipe, search_query=search_query)
    return "Recipe not found!", 404

@app.route('/about/')
def index():
    # Fetch regions, subregions, or any other data you want to display
   return render_template('about.html')

# Fetch recipes for a specific country
@app.route('/recipe/<country_name>')
def country_recipe(country_name):
  
    country = Country.objects(name=country_name).first()
    if country:
        recipes = Recipe.objects(country=country)
        return render_template('recipe.html', recipes=recipes, country=country)
    else:
        # Handle the case where the country is not found
        return render_template('recipe.html', country_name=country_name), 404


if __name__ == '__main__':
    app.run(debug=True)


