from flask import Flask, render_template, request
from flask_mongoengine import MongoEngine
from models.schema import Region, SubRegion, Country, Recipe

app = Flask(__name)

# MongoDB configuration
app.config['MONGODB_SETTINGS'] = {
    'db': 'recipe_db',
    'host': 'mongodb://localhost:27017/recipe_db',  # Update with your MongoDB connection string
}
db = MongoEngine(app)

# Define routes and views
@app.route('/')
def index():
    # Fetch regions, subregions, or any other data you want to display
    regions = Region.objects()
    return render_template('index.html', regions=regions)

@app.route('/recipes/<country_name>')
def country_recipes(country_name):
    # Fetch recipes for a specific country
    country = Country.objects(name=country_name).first()
    if country:
        recipes = Recipe.objects(country=country)
        return render_template('recipes.html', recipes=recipes, country=country)
    else:
        return "Country not found", 404

if __name__ == '__main__':
    app.run(debug=True)

