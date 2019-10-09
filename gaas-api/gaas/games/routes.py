#################
# imports ####
#################

from functools import partial
from . import games_blueprint
from gaas.games.enabled import get_enabled
import json
from pprint import pprint
from flask_json import json_response
from flask import jsonify
try:
    from ujson import dumps as json_dumps
except ImportError:
    from json import dumps
    json_dumps = partial(dumps, separators=(",", ":"))

################
# routes ####
################

@games_blueprint.route('/list')
def getGames():
    return json_dumps(get_enabled())
