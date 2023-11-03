""" RECIPE MODEL """
import datetime
import mongoengine


class Recipe(mongoengine.Document):
  """"
      This model is used to setup recipes collection.
  """

  created_at = mongoengine.DateTimeField(default=datetime.datetime.now())
  updated_at = mongoengine.DateTimeField(default=datetime.datetime.now())
  name = mongoengine.StringField(required=True, unique=True, min_length=3, max_length=50)
  description = mongoengine.StringField(required=True, min_length=10, max_length=150)
  procedure = mongoengine.StringField(required=True, min_length=10, max_length=1000)
  recipe_image = mongoengine.ImageField(required=True)

  meta = {
    'db_alias': 'main',
    'collection': 'recipes'
  }
