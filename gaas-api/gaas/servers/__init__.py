"""
The users Blueprint handles the user management for this application.
Specifically, this Blueprint allows for new users to register and for
users to log in and to log out of the application.
"""
from flask import Blueprint
servers_blueprint = Blueprint('servers', __name__)

from . import routes
