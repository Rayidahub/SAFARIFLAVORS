from flask import Flask, render_template, request, redirect, url_for
from flask_mongoengine import MongoEngine
from mongoengine import connect, Document, StringField, ReferenceField, ListField
from flask_admin import Admin
from flask_admin.contrib.mongoengine import ModelView
# from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models.schema import Region, SubRegion, Country, Recipe
from models.user import User
from models.model import Food
import os


app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'recipe_db',
    'host': 'mongodb://localhost:27017/recipe_db'   
}

# Initialize the MongoEngine
db = MongoEngine(app)

# Define the Food model
class Food(db.Document):
    name = db.StringField()
    category = db.StringField()
    country = db.StringField()
    description = db.StringField()
    image = db.StringField()


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure secret key

# Configure the uploads folder
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'static')
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg', 'png', 'gif'}

# Set up the configuration for your MongoDB database


# Connect to MongoDB using mongoengine
# Create the Flask-Admin instance
admin = Admin(app, name='Recipe Admin', template_mode='bootstrap3')

# Add model views for Recipe, Region, SubRegion, and Country
admin.add_view(ModelView(Recipe))
admin.add_view(ModelView(Region))
admin.add_view(ModelView(SubRegion))
admin.add_view(ModelView(Country))

# # Initialize Flask-Login
# login_manager = LoginManager()
# login_manager.init_app(app)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# # Define routes and views
# @login_manager.user_loader
# def load_user(user_id):
#     return User.objects(pk=user_id).first()

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

@app.route('/recipe/submit-food', methods=['POST'])
def submit_food():
    # Get data from the form
    food_name = request.form.get('food-name')
    food_category = request.form.get('food-category')
    food_country = request.form.get('food-country')
    food_description = request.form.get('food-description')
    food_ingredient = request.form.get('food-ingredient')
    food_intructions = request.form.get('food-instructions')
    food_image = request.files['food-image']

    if food_image and allowed_file(food_image.filename):
        # Save the image to the uploads folder
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], food_image.filename)
        food_image.save(image_path)

        # Create a new Food object and save it to the database
        new_food = Food(
            name=food_name,
            category=food_category,
            country=food_country,
            description=food_description,
            ingredient=food_ingredient,
            instuction=food_intructions,
            image=image_path

        )
        new_food.save()

        return redirect('/success')  # Redirect to a success page after submission

    return "Invalid file type or no file provided."


@app.route('/food_detail/<food_id>', methods=['GET'])
def food_detail(food_id):
    food = Food.objects.get(id=food_id)
    return render_template('recipe_view.html', food=food)

@app.route('/static/')
def other_page():
  return render_template('recipe_view.html')

@app.route('/success')
def success():
    return render_template('recipe.html')
    
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         user = User.objects(username=username).first()
#         if user and user.password == password:
#             login_user(user)
#             return redirect(url_for('admin.index'))
#     return render_template('login.html')    


# @app.route('/logout')
# # @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)


