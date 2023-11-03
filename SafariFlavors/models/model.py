from mongoengine import Document, StringField, ReferenceField, ListField

class Region(Document):
    name = StringField()

class SubRegion(Document):
    name = StringField()
    region = ReferenceField(Region)

class Country(Document):
    name = StringField()
    subregion = ReferenceField(SubRegion)

class Recipe(Document):
    country = ReferenceField(Country)
    food_title = StringField()
    ingredients = ListField(StringField())
    instructions = StringField()
