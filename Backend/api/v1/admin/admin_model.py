""" ADMIN MODEL """
import mongoengine


class Admin(mongoengine.Document):
  """ Setup for admin user """
  email = mongoengine.StringField(required=True, unique=True)
  password = mongoengine.StringField(required=True)
  status = mongoengine.BooleanField(required=True)

  meta = {
    'db_alias': 'main',
    'collection': 'admins'
  }
