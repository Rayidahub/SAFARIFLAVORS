"""
  recipe routes
"""
from v1.views import sf_views
from v1.models.country import Country


@sf_views.route("/recipes/<string:country>/<string:recipe_name>", methods=['GET'], strict_slashes=False)
async def get_recipe(country: str, recipe_name: str):
  """
    get the specific recipe for a country.
  """
  try:
    country = Country.objects(country_name=country.title()).first()
    recipe = next((recipe async for recipe in country.recipes if recipe.recipe_name == recipe_name), None)

    if recipe:
      recipe_data = {
        "country_name": country.country_name,
        "sub_region": country.sub_region,
        "recipe_name": recipe.recipe_name,
        "recipe_description": recipe.recipe_description,
        "recipe_procedure": recipe.recipe_procedure,
        "recipe_image": recipe.recipe_image
      }
      return recipe_data
    
    else:
      return {'message': f'No recipes found for {recipe_name}'}, 404

  except Exception as err:
    return {"error": str(err)}, 500
