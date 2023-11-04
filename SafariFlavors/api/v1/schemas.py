"""
  Schemas for CRUD operations
"""
from marshmallow import Schema, fields, validate, ValidationError


# Admin Schema
class AdminSchema(Schema):
  """_summary_
    Schema to validate request data for admin login.

    Args:
      Schema (object): Marshmallow
  """
  email = fields.String(required=True)
  password = fields.String(required=True)


# Recipe Schema
class CreateRecipeSchema(Schema):
  """_summary_
    Create recipe for a particular country.

    Args:
      Schema (object): Marshmallow
  """
  region = fields.String(required=True)
  sub_region = fields.String(required=True)
  country = fields.String(required=True, validate=validate.Length(max=50))
  recipe_name = fields.String(required=True, validate=validate.Length(min=3, max=50))
  recipe_description = fields.String(required=True, validate=validate.Length(min=10, max=150))
  recipe_procedure = fields.String(required=True, validate=validate.Length(min=10))

  def dump(self, obj, many=None):
    # Set the 'region' field to 'Africa'
    obj['region'] = 'Africa'
    return super().dump(obj, many)


class ImageField(fields.Field):
  """_summary_
    Handle Image Validation with formats.

    Args:
      fiels.Field (object): Marshmallow
  """
  def _deserialize(self, value):
    if not value:
      return None

    if not value.filename:
      raise ValidationError("Invalid image file")

    filename = value.filename.lower()

    if not filename.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
      raise ValidationError("Invalid image format. Supported formats: PNG, JPG, JPEG, GIF, BMP")

    return value


class RecipeImageSchema(Schema):
  """_summary_
    Validate the Image sent to create recipe.

    Args:
      Schema (object): Marshmallow
  """
  recipe_image = ImageField(required=True)


class UpdateRecipeSchema(Schema):
  """_summary_
    Update the recipe for the specified country.

    Args:
      Schema (object): Marshmallow
  """
  country = fields.String(required=True)
  prev_recipe_name = fields.String(required=True)
  new_recipe_name = fields.String(validate=validate.Length(min=3, max=50))
  new_recipe_description = fields.String(validate=validate.Length(min=10, max=150))
  new_recipe_procedure = fields.String(validate=validate.Length(min=10))


class UpdateImageSchema(Schema):
  """_summary_
    Update the recipe image.

    Args:
      Schema (object): Marshmallow
  """
  recipe_image = ImageField()


class DeleteRecipeSchema(Schema):
  """_summary_
    Delete the recipe specified.

    Args:
      Schema (object): Marshmallow
  """
  country = fields.String(required=True)
  recipe_name = fields.String(required=True)


# Country Schema
class UpdateCountrySchema(Schema):
  """_summary_
    Update

    Args:
      Schema (object): _description_
  """
  sub_region = fields.Enum(required=True, choices=['Northern Africa', 'Eastern Africa', 'Southern Africa', 'Western Africa'])
  country = fields.String(required=True)


# Initialize the models
admin_val_schema = AdminSchema()
create_recipe_schema= CreateRecipeSchema()
recipe_image_schema = RecipeImageSchema()
update_recipe_schema = UpdateRecipeSchema()
update_recipe_image_schema = UpdateImageSchema()
delete_recipe_schema = DeleteRecipeSchema()
update_country_schema = UpdateCountrySchema()
