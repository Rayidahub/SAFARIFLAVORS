from flask import Flask, render_template, request, redirect, url_for
from flask_mongoengine import MongoEngine
from mongoengine import connect, Document, StringField, ReferenceField, ListField
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.mongoengine import ModelView
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models.schema import Region, SubRegion, Country, Recipe
from models.user import User



app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure secret key


# Set up the configuration for your MongoDB database
app.config['MONGODB_SETTINGS'] = {
    'db': 'recipe_db',
    'host': 'mongodb://localhost:27017/recipe_db'
}

# Connect to MongoDB using mongoengine
connect('mydatabase', host='mongodb://localhost:27017/recipe_db')

# Create the Flask-Admin instance
admin = Admin(app, name='Recipe Admin', template_mode='bootstrap3')

# Add model views for Recipe, Region, SubRegion, and Country
admin.add_view(ModelView(Recipe))
admin.add_view(ModelView(Region))
admin.add_view(ModelView(SubRegion))
admin.add_view(ModelView(Country))

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Define routes and views

@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()

@app.route("/")
def home():
     return render_template('home.html')

@app.route('/')
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
    
@app.route('/submit-food', methods=['POST', 'GET'])
def submit_food():
    # Get data from the form
    food_name = request.form.get('food-name')
    food_category = request.form.get('food-category')
    food_country = request.form.get('food-country')
    food_description = request.form.get('food-description')
    # Assuming you are storing the image file path, you can upload it to your server and save the path here
    food_image = '/path/to/uploaded/image.jpg'  # Replace with the actual path
    
    # Create a new Food object and save it to the database
    new_food = Food(
        name=food_name,
        category=food_category,
        country=food_country,
        description=food_description,
        image=food_image
    )
    new_food.save()

    return redirect('/success')  # Redirect to a success page after submission
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.objects(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('admin.index'))
    return render_template('login.html')    

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)


