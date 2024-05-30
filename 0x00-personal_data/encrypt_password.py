#!/usr/bin/env python3

"""
This module provides functions for securely hashing and verifying passwords
using the bcrypt algorithm, which is a robust and widely-used method for
password storage and authentication.
"""

import bcrypt

def hash_password(password: str) -> bytes:
    """
    Hashes the given plaintext password using a randomly generated salt.

    Args:
        password (str): The plaintext password to be hashed.

    Returns:
        bytes: The hashed password as a bytes object.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Checks if the given plaintext password matches the provided hashed password.

    Args:
        hashed_password (bytes): The hashed password to compare against.
        password (str): The plaintext password to verify.

    Returns:
        bool: True if the password is valid (matches the hashed password), False otherwise.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
