#!/usr/bin/env python3
""" This module contains the views for the index.
"""
from flask import jsonify, abort
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """ This route returns the status of the API when a GET request is made.
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats/', strict_slashes=False)
def stats() -> str:
    """ This route returns the count of each object when a GET request is made.
    """
    from models.user import User
    stats = {}
    stats['users'] = User.count()
    return jsonify(stats)


@app_views.route("/unauthorized/",
                 strict_slashes=False)
def unauthorized() -> str:
    ''' This route handles unauthorized requests and returns a 401 status code.
    '''
    abort(401)


@app_views.route("/forbidden/",
                 strict_slashes=False)
def forbidden() -> str:
    ''' This route handles forbidden requests and returns a 403 status code.
    '''
    abort(403)

