""" Setup Blueprint for none authen """
from flask import Blueprint


sf_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from v1.views.dashboard import *
