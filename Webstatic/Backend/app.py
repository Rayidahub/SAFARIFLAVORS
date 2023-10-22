from flask import Flask, render_template, request, redirect, url_for
from flask_mongoengine import MongoEngine
from flask_admin import Admin
from flask_admin.contrib.mongoengine import ModelView
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models.schema import Region, SubRegion, Country, Recipe
from models.user import User

app = Flask(__name)
app.secret_key = 'your_secret_key'  # Change this to a secure secret key

# MongoDB configuration
app.config['MONGODB_SETTINGS'] = {
    'db': 'recipe_db',
    'host': 'mongodb://localhost:27017/recipe_db',
}
db = MongoEngine(app)

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


