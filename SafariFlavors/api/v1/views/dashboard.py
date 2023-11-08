"""
  dashboard routes
"""
from v1.views import sf_views
from v1.models.country import Country
from v1.views.fetch_recipe_helper import fetch_recipes
import asyncio


@sf_views.route("/recipes", methods=['GET'], strict_slashes=False)
async def all_recipes():
  """
    Fetch all the recipes for all the countries.
  """
  try:
    countries = [country async for country in Country.objects()]

    if not countries:
      return {'message': 'No recipes found'}, 404

    return await asyncio.run(fetch_recipes(countries))

  except Exception as err:
    return {"error": str(err)}, 500


@sf_views.route("/recipes/<string:sub_region>", methods=['GET'], strict_slashes=False)
async def sub_region_recipes(sub_region: str):
  """
    _summary_
      Fetch all the recipes in a specific sub region
    Args:
      sub_region (str): the sub region name.
  """
  try:
    sub_countries = Country.objects(sub_region=sub_region)

    if not sub_countries:
      return {'message': f'No recipes found for {sub_region}'}, 404

    return await asyncio.run(fetch_recipes(sub_countries))

  except Exception as err:
    return {"error": str(err)}, 500


@sf_views.route("/recipes/<string:country>", methods=['GET'], strict_slashes=False)
async def country_recipes(country: str):
  """
    _summary_
      Fetch all recipes for a specific country

    Args:
      country (str): country name
  """
  try:
    country = Country.objects(country_name=country.title()).first()

    if not country:
      return {'message': f'No recipes forund for {country}'}, 404
    return await asyncio.run(fetch_recipes(country))

  except Exception as err:
    return {"error": str(err)}, 500
