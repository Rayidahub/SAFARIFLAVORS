from flask import Flask, make_response, jsonify
from flask_mongoengine import MongoEngine
from dotenv import load_dotenv, find_dotenv
from os import environ
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from v1 import sf_views
from v1.admin import sf_admin


# find and load .env file
load_dotenv(find_dotenv('safari.env'))

# Initiate app and dependencies
app = Flask(__name__)
app.secret_key = environ.get('SECRETKEY')
JWTManager(app)
CORS(app)
db = MongoEngine()

# register blueprints
app.register_blueprint(sf_views)
app.register_blueprint(sf_admin)

# MongoDB configuration
app.config["MONGODB_SETTINGS"] = [
  {
    "db": environ.get('DB'),
    "host": environ.get('HOST'),
    "port": 27017,
    "alias": "main",
  }
]

# Link the Base to the app
db.init_app(app)

# Error handling for 404
@app.errorhandler(404)
def not_found(error):
  """
  404 Error response:
      resource not found
  """
  return make_response(jsonify({'error': "Not found"}), 404)


# Start app
if __name__ == '__main__':
  host = environ.get('HOST', '127.0.0.1')
  port = environ.get('PORT', '3000')
  app.run(host=host, port=port, debug=True)
