#!/usr/bin/env python3
"""This module sets up the routing for the API."""

from flask import Blueprint

# Create a Blueprint for the views
app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

# Import the views
from api.v1.views.index import *
from api.v1.views.users import *

# Load the user data from file
User.load_from_file()

# Import the session authentication views
from api.v1.views.session_auth import *

