""" Setup Blueprint For Admin"""
from flask import Blueprint


sf_admin = Blueprint('admin_views', __name__, url_prefix='/api/v1/admin')

from admin_view import *
