#!/usr/bin/env python3
""" This is the main module for the Cookie server """

from flask import Flask, request
from api.v1.auth.auth import Auth

# Create an Auth object
auth = Auth()

# Initialize a Flask application
app = Flask(__name__)

# Define a route for the root path
@app.route('/', methods=['GET'], strict_slashes=False)
def root_path():
    """ This function handles GET requests to the root path """
    return "Cookie value: {}\n".format(auth.session_cookie(request))

# Run the Flask application
if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")

