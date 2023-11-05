""" Setup Blueprint For Admin"""
from flask import Blueprint


sf_admin = Blueprint('admin_views', __name__, url_prefix='/api/v1/admin')

from v1.admin.admin_view import *
