""" COUNTRY MODEL """
import datetime
import mongoengine
from recipe import Recipe


class Country(mongoengine.Document):
  """"
      This model is used to setup countries collection.
  """

  created_at = mongoengine.DateTimeField(default=datetime.datetime.now())
  updated_at = mongoengine.DateTimeField(default=datetime.datetime.now())
  region = mongoengine.StringField(default='Africa')
  sub_region = mongoengine.EnumField(required=True, choices=['Northern Africa', 'Eastern Africa', 'Southern Africa', 'Western Africa'])
  country = mongoengine.StringField(unique=True, required=True, max_length=50)
  recipes = mongoengine.EmbeddedDocumentListField(Recipe)

  meta = {
      'db_alias': 'main',
      'collection': 'countries'
  }
