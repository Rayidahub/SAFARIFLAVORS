from flask import Flask, render_template, request, redirect, url_for
from flask_mongoengine import MongoEngine
from flask_admin import Admin
from flask_admin.contrib.mongoengine import ModelView
from models.schema import Region, SubRegion, Country, Recipe

app = Flask(__name)

# MongoDB configuration
app.config['MONGODB_SETTINGS'] = {
    'db': 'recipe_db',
    'host': 'mongodb://localhost:27017/recipe_db',  # Update with your MongoDB connection string
}
db = MongoEngine(app)

# Create the Flask-Admin instance
admin = Admin(app, name='Recipe Admin', template_mode='bootstrap3')

# Add model views for Recipe, Region, SubRegion, and Country
admin.add_view(ModelView(Recipe))
admin.add_view(ModelView(Region))
admin.add_view(ModelView(SubRegion))
admin.add_view(ModelView(Country))

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

