from mongoengine import Document, StringField

class Food(Document):
    name = StringField(max_length=120, required=True)
    category = StringField(max_length=50, required=True)
    country = StringField(max_length=50, required=True)
    description = StringField(required=True)
    image = StringField(max_length=200, required=True)
