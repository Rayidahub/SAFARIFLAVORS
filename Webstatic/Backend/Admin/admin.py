from flask import Blueprint, render_template
from flask_admin import Admin
from flask_admin.contrib.mongoengine import ModelView
from models.schema import Recipe

admin_bp = Blueprint('admin', __name__)

# Create the admin interface
admin = Admin(name='Recipe Admin', template_mode='bootstrap3')

# Add a view for the Recipe model
admin.add_view(ModelView(Recipe))

@admin_bp.route('/')
def admin_home():
    return render_template('admin_home.html')

@admin_bp.route('/create_recipe', methods=['GET', 'POST'])
def create_recipe():
    # Logic for creating a recipe
    return render_template('create_recipe.html')

@admin_bp.route('/update_recipe/<recipe_id>', methods=['GET', 'POST'])
def update_recipe(recipe_id):
    # Logic for updating a recipe
    return render_template('update_recipe.html')

@admin_bp.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    # Logic for deleting a recipe
    return "Recipe deleted successfully"

