from typing import List, Dict, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from v1.models.country import Country


async def fetch_recipes(countries: Union[List[Country], Country]) -> List[Dict]:
  """_summary_
    This function populate recipes with the right data and return a list of
    dictionary.

  Args:
      countries (Union[List[Country], Country]): A list of Country object or a single
      country object.

  Returns:
      List[Dict]: A list of dictionary containing data of recipes.
  """
  # recipes list to store data.
  recipes_info = []

  if isinstance(countries, list):
    async for country in countries:
      sub_region = country.sub_region
      country_name = country.country_name

      # Get all the recipes for the country
      recipes = country.recipes


      # Iterate through the recipes of the country
      async for recipe in recipes:
        recipe_data = {
          "country_name": country_name,
          "sub_region": sub_region,
          "recipe_name": recipe.recipe_name,
          "recipe_description": recipe.recipe_description,
          "recipe_procedure": recipe.recipe_procedure,
          "recipe_image": recipe.recipe_image
        }

        # add the recipe to the list
        recipes_info.append(recipe_data)

  else:
    async for recipe in countries.recipes:
      recipe_data = {
        "country_name": countries.country_name,
        "sub_region": countries.sub_region,
        "recipe_name": recipe.recipe_name,
        "recipe_description": recipe.recipe_description,
        "recipe_procedure": recipe.recipe_procedure,
        "recipe_image": recipe.recipe_image
      }

      # add the recipe to the list
      recipes_info.append(recipe_data)

  return recipes_info
