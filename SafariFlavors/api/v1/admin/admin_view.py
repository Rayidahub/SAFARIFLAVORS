"""
  Routes for CRUD operations
"""
from v1.admin import sf_admin
from flask import request, jsonify, abort
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from marshmallow import ValidationError
from v1 import schemas
from v1.admin.admin_model import Admin
from v1.data import Africa
from v1.models.country import Country
from v1.models.recipe import Recipe
import bcrypt


# Admin Routes
@sf_admin.route("/login", methods=['POST'], strict_slashes=False)
def login():
  '''
    Login the Admin
  '''
  try:
    login_data: object = schemas.admin_val_schema.load(request.get_json())
    admin: object = Admin.objects(email=login_data['email']).first()

    if not admin:
      abort(404, message=f"{login_data['email']} does not exist")

    if not bcrypt.checkpw((login_data['password'].encode('utf-8'), admin.password.encode('utf-8'))):
      return jsonify({"message": "Invalid password."}), 422
    
    jwt = create_access_token(
      identity={'email': admin['email'], 'super_status': admin['super_status']}, expires_delta=18000)

    return jsonify({'token': jwt}), 201

  except ValidationError as err:
    return jsonify({'message': err.args[0]}), 400
  except Exception as err:
    return jsonify({'message': err}), 500


# Recipe Routes
@sf_admin.route("/create_recipe", methods=['POST'], strict_slashes=False)
@jwt_required()
def create_recipe():
  '''
    Create recipe and attach the recipe to a country.
  '''
  try:
    new_data: object = schemas.create_recipe_schema.load(request.get_json())
    new_recipe_image: object = schemas.recipe_image_schema.load(request.files)

    sub_region: str = new_data['sub_region'].title()
    country: str = new_data['country'].title()

    # Verify if the country name for the sub region
    if country not in Africa[sub_region]:
      return jsonify({"message": 'Country is invalid.'}), 422

    # created object to save data
    country_data = {
      'region': new_data['region'], 
      'sub_region': new_data['sub_region'],
      'country': new_data['country'],
    }

    recipe_data = {
      'recipe_name': new_data['recipe_name'],
      'recipe_description': new_data['recipe_description'],
      'recipe_procedure': new_data['recipe_procedure'],
      'recipe_image': new_recipe_image['image']
    }

    # Check if the country name is present to prevent Error due to unique country name
    country_searched: object = Country.objects(country=country).first()

    new_recipe = Recipe(**recipe_data)

    if not country_searched:
      new_country = Country(**country_data)
      new_country.recipes.append(new_recipe)
      new_country.save()

    else:
      country_searched.recipes.append(new_recipe)
      country_searched.save()

    return jsonify({'message': 'recipe created'}), 201

  except ValidationError as err:
    return jsonify({'message': err.args[0]}), 400
  except Exception as err:
    return jsonify({'message': err}), 500


@sf_admin.route("/update_recipe", methods=['PUT'], strict_slashes=False)
@jwt_required()
def update_recipe():
  '''
    Update a Recipe
  '''
  try:
    to_update_data: object = schemas.update_recipe_schema.load(request.get_json())
    to_update_image: object = schemas.update_recipe_image_schema.load(request.files)

    new_image = to_update_image.get('image')

    existing_country: object = Country.objects(
      country=to_update_data['country'].title()).first()

    if not existing_country:
      abort(404, message='Country not Found')

    found_recipe = existing_country.recipes.filter(
      recipe_name=to_update_data.prev_recipe_name).first()

    if found_recipe:
      if to_update_data['new_recipe_name']:
        found_recipe.recipe_name = to_update_data['new_recipe_name']
      if to_update_data['new_recipe_description']:
        found_recipe.recipe_description = to_update_data['new_recipe_description']
      if to_update_data['new_recipe_procedure']:
        found_recipe.recipe_procedure = to_update_data['new_recipe_procedure']
      if new_image:
        found_recipe.recipe_image = new_image

      existing_country.save()
      return jsonify({'message': 'recipe updated'}), 200

    else:
      abort(404, message=f'Recipe {to_update_data.prev_recipe_name} not found')

  except ValidationError as err:
    return jsonify({'message': err.args[0]}), 400
  except Exception as err:
    return jsonify({'message': err}), 500


@sf_admin.route("/delete_recipe", methods=['DELETE'], strict_slashes=False)
@jwt_required()
def delete_recipe():
  '''
    Delete a Recipe
  '''
  try:
    to_delete_data: object = schemas.delete_recipe_schema.load(request.get_json())

    existing_country: object = Country.objects(
      country=to_delete_data['country'].title()).first()

    if not existing_country:
      abort(404, message='Country not Found')

    found_recipe: object = existing_country.recipes.filter(
      recipe_name=to_delete_data.recipe_name).first()

    if found_recipe:
      existing_country.recipes.remove(found_recipe)
      existing_country.save()
      return jsonify({'message': 'Recipe deleted'}), 200

    else:
      jsonify({'message': 'Something went wrong Recipe not found'}), 400

  except ValidationError as err:
    return jsonify({'message': err.args[0]}), 400
  except Exception as err:
    return jsonify({'message': err}), 500


# Country Routes
@sf_admin.route("/update_country/<string:id>", methods=['PUT'], strict_slashes=False)
@jwt_required()
def update_country(id):
  """
    _summary_
    update the country data

    Args:
      id (string): country id to update
  """
  try:
    to_update_country: object = schemas.update_country_schema.load(request.get_json())
    found_country = Country.objects(id=id).first()

    if found_country:
      found_country.country = to_update_country['country']
      found_country.sub_region = to_update_country['sub_region']
      found_country.save()
      return jsonify({'message': 'Country updated'}), 200

    else:
      abort(404, message='Country not Found')

  except ValidationError as err:
    return jsonify({'message': err.args[0]}), 400
  except Exception as err:
    return jsonify({'message': err}), 500


@sf_admin.route("/delete_country/<string:id>", methods=['DELETE'], strict_slashes=False)
@jwt_required()
def delete_country(id):
  """
    _summary_
    delete the country data
    NB: Be careful here, because deleting a country, will delete all the embedded Recipes in
    it.

    Args:
      id (string): country id to delete
  """
  try:
    payload = get_jwt_identity()

    if not payload['super_status']:
      return jsonify({'message': 'Forbidden'}), 403

    found_country = Country.objects(id=id).first()
    if not found_country:
      abort(404, message='Country not Found')

    found_country.delete()
    return jsonify({'message': 'Country deleted'}), 200

  except ValidationError as err:
    return jsonify({'message': err.args[0]}), 400
  except Exception as err:
    return jsonify({'message': err}), 500
