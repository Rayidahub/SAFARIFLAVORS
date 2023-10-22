from mongoengine import connect
from models.schema import Region, SubRegion, Country, Recipe

# Connect to the MongoDB server and database
connect(db="recipe_db")

# Create or access regions, subregions, countries, and recipes
africa = Region(name="Africa").save()

north = SubRegion(name="North", region=africa).save()
south = SubRegion(name="South", region=africa).save()
east = SubRegion(name="East", region=africa).save()
west = SubRegion(name="West", region=africa).save()

country1 = Country(name="Country1", subregion=north).save()
country2 = Country(name="Country2", subregion=south).save()
country3 = Country(name="Country3", subregion=east).save()
country4 = Country(name="Country4", subregion=west).save()

recipe = Recipe(
    country=country1,
    food_title="Recipe Title",
    ingredients=["Ingredient 1", "Ingredient 2"],
    instructions="Cooking instructions..."
).save()

# Query recipes for a specific country
country_name = "Country1"
recipes_for_country = Recipe.objects(country=country1)

for recipe in recipes_for_country:
    print(f"Food Title: {recipe.food_title}")
    print(f"Ingredients: {', '.join(recipe.ingredients)}")
    print(f"Instructions: {recipe.instructions}\n")

