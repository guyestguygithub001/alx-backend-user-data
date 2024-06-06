#!/usr/bin/env python3
"""This module provides authentication functionality for the API."""

import os
import re
from typing import List, TypeVar
from flask import request

class Auth:
    """This class provides methods for handling authentication."""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Determines if authentication is required for a given path."""
        if path is not None and excluded_paths is not None:
            for exclusion_path in map(lambda x: x.strip(), excluded_paths):
                pattern = ''
                if exclusion_path[-1] == '*':
                    pattern = '{}.*'.format(exclusion_path[0:-1])
                elif exclusion_path[-1] == '/':
                    pattern = '{}/*'.format(exclusion_path[0:-1])
                else:
                    pattern = '{}/*'.format(exclusion_path)
                if re.match(pattern, path):
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """Retrieves the 'Authorization' field from the request headers."""
        if request is not None:
            return request.headers.get('Authorization', None)
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns the current user associated with the request. This method should be overridden in a subclass."""
        return None

    def session_cookie(self, request=None) -> str:
        """Retrieves the value of the cookie named 'SESSION_NAME' from the request."""
        if request is not None:
            cookie_name = os.getenv('SESSION_NAME')
            return request.cookies.get(cookie_name)

