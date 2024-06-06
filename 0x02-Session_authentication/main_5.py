#!/usr/bin/env python3
""" This is the main module """

import uuid
from api.v1.auth.basic_auth import BasicAuth
from models.user import User

# Create a test user
user_email = str(uuid.uuid4())
user_clear_pwd = str(uuid.uuid4())
user = User()
user.email = user_email
user.first_name = "Bob"
user.last_name = "Dylan"
user.password = user_clear_pwd
print("New user: {}".format(user.display_name()))
user.save()

# Retrieve this user using the BasicAuth class

a = BasicAuth()

# Test with null credentials
u = a.user_object_from_credentials(None, None)
print(u.display_name() if u is not None else "None")

# Test with non-string credentials
u = a.user_object_from_credentials(89, 98)
print(u.display_name() if u is not None else "None")

# Test with non-existent email
u = a.user_object_from_credentials("email@notfound.com", "pwd")
print(u.display_name() if u is not None else "None")

# Test with correct email but incorrect password
u = a.user_object_from_credentials(user_email, "pwd")
print(u.display_name() if u is not None else "None")

# Test with correct email and password
u = a.user_object_from_credentials(user_email, user_clear_pwd)
print(u.display_name() if u is not None else "None")

