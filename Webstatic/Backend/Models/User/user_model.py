from mongoengine import Document, StringField

class User(Document):
    username = StringField(unique=True, required=True)
    password = StringField(required=True)

