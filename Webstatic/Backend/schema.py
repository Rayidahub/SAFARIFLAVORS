""from mongoengine import Document, StringField, ReferenceField, ListField

class Region(Document):
    name = StringField(required=True)

class SubRegion(Document):
    name = StringField(required=True)
    region = ReferenceField(Region, required=True)

class Country(Document):
    name = StringField(required=True)
    subregion = ReferenceField(SubRegion, required=True)

class Recipe(Document):
    country = ReferenceField(Country, required=True)
    food_title = StringField(required=True)
    ingredients = ListField(StringField())
    instructions = StringField()

