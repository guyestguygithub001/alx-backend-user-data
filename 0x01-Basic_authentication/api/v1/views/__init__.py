#!/usr/bin/env python3
""" This script is responsible for setting up the application views.
"""
from flask import Blueprint

# Create a Blueprint for the application views
app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

# Import the necessary views
from api.v1.views.index import *
from api.v1.views.users import *

# Load user data from file
User.load_from_file()

