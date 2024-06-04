#!/usr/bin/env python3
"""
This is the main module for the API.
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os

# Initialize Flask app and register the blueprint
app = Flask(__name__)
app.register_blueprint(app_views)

# Enable CORS for the app, allowing all origins
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None

# Depending on the environment variable 'AUTH_TYPE', import the appropriate authentication method
if getenv('AUTH_TYPE') == "auth":
    from api.v1.auth.auth import Auth
    auth = Auth()

elif getenv('AUTH_TYPE') == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()

# Before each request, check if it requires authentication
@app.before_request
def filter_request():
    if auth is None:
        return

    excluded_paths = [
        '/api/v1/status/',
        '/api/v1/unauthorized/',
        '/api/v1/forbidden/'
    ]
    if not auth.require_auth(request.path, excluded_paths):
        return

    # If the request lacks an authorization header or the current user is not found, abort the request
    if auth.authorization_header(request) is None:
        abort(401)

    if auth.current_user(request) is None:
        abort(403)

# Define error handlers for 404 (Not Found), 401 (Unauthorized), and 403 (Forbidden) errors
@app.errorhandler(404)
def not_found(error) -> str:
    """Handle requests to non-existent routes."""
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(401)
def unauthorized_request(error) -> str:
    '''Handle requests lacking proper authorization.'''
    return jsonify({
        "error": "Unauthorized"
    }), 401

@app.errorhandler(403)
def forbidden_request(error) -> str:
    '''Handle requests to routes that are forbidden to the current user.'''
    return jsonify({
        "error": "Forbidden"
    }), 403

# Run the app when the script is executed directly
if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)

