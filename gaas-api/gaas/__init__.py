from flask import Flask
from flask.json import JSONEncoder as BaseJSONEncoder
from flask_cors import CORS
from kubernetes import config, client



#######################
# Configuration ####
#######################


######################################
# Application Factory Function ####
######################################


def create_app(config_filename=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile(config_filename)
    
    app.config['JSON_ADD_STATUS'] = True
    app.config['JSON_STATUS_FIELD_NAME'] = 'http_status'

    app.config['GAAS_NAMESPACE'] = "gaas"
    app.config['GAAS_SERVICE_SCOPE'] = "10.96.0.0/14"

    # Set the default JSON encoder
    app.json_encoder = JSONEncoder
    

    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    initialize_extensions(app)
    register_blueprints(app)
    return app


##########################
# Helper Functions ####
##########################
def initialize_extensions(app):
    # Since the application instance is now created, pass it to each Flask
    # extension instance to bind it to the Flask application instance (app)
    
    # Kubernetes client
    #try:
    try:
        config.load_incluster_config()
    except Exception:
        config.load_kube_config()
    
def register_blueprints(app):
    # Since the application instance is now created, register each Blueprint
    # with the Flask application instance (app)
    from gaas.games import games_blueprint
    from gaas.servers import servers_blueprint
    app.register_blueprint(games_blueprint, url_prefix='/games')
    app.register_blueprint(servers_blueprint, url_prefix='/servers')

class JSONEncoder(BaseJSONEncoder):
    """Custom :class:`JSONEncoder` which respects objects that include the
    :class:`JsonSerializer` mixin.
    """
    def default(self, obj):
        if isinstance(obj, JsonSerializer):
            return obj.to_json()
        return super(JSONEncoder, self).default(obj)


class JsonSerializer(object):
    """A mixin that can be used to mark a SQLAlchemy model class which
    implements a :func:`to_json` method. The :func:`to_json` method is used
    in conjuction with the custom :class:`JSONEncoder` class. By default this
    mixin will assume all properties of the SQLAlchemy model are to be visible
    in the JSON output. Extend this class to customize which properties are
    public, hidden or modified before being being passed to the JSON
    serializer.
    """

    __json_public__ = None
    __json_hidden__ = None
    __json_modifiers__ = None
    __json_consolidate__ = None

    def get_field_names(self):
        for p in self.__mapper__.iterate_properties:
            yield p.key

    def to_json(self):
        field_names = self.get_field_names()

        public = self.__json_public__ or field_names
        hidden = self.__json_hidden__ or []
        modifiers = self.__json_modifiers__ or dict()
        consolidate = self.__json_consolidate__ or []

        fields = [a for a in public if a not in hidden]

        rv = dict()
        for key in fields:
            rv[key] = getattr(self, key)
        for key, modifier in modifiers.items():
            if key in fields:
                value = getattr(self, key)
                rv[key] = modifier(value, self)
        for prefix in consolidate:
            rv[prefix] = {}
            for key, value in list(rv.items()):
                if prefix + '_' in key:
                    new_key = key[len(prefix) + 1:]
                    rv[prefix][new_key] = rv.pop(key)
            if not rv[prefix]:
                rv.pop(prefix)
        return rv