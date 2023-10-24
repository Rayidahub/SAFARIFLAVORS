""" Setup Blueprint"""
from flask import Blueprint


sf_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

