from flask import Flask, Blueprint
from flask_restx import Api
from prometheus_flask_exporter import PrometheusMetrics


class FlaskSetup:
    """ Holds setup of a Flask App
    """

    def __init__(self, name, port, version='1.0'):
        self.app = Flask(__name__)
        self.name = name
        self.port = port
        self.version = version

        self.metrics = None
        self.api = None

    def add_swagger(self, title, description, url_prefix=None):
        if url_prefix:
            blueprint = Blueprint('api', __name__, url_prefix=url_prefix)
            self.api = Api(
                blueprint,
                doc='/swagger',
                version=self.version,
                title=title,
                description=description
            )
            self.app.register_blueprint(blueprint)
        else:
            self.api = Api(
                self.app,
                version=self.version,
                doc='/swagger',
                title=title,
                description=description
            )
        self.app.config.SWAGGER_UI_DOC_EXPANSION = 'list'  # Expand all endpoints

    def add_prometheus(self):
        self.metrics = PrometheusMetrics(self.app)

    def add_command(self, name, command):
        self.app.cli.command(name)(command)

    def add_init_func(self, func):
        self.app.before_first_request(func(self.app))

    def log_internal_error(self, err, namespace, route):
        path = '/{namespace}{route}'.format(
            namespace=namespace.name,
            route=route
        )
        self.app.logger.error(
            'Internal Error requesting {path}: {err}'.format(
                path=path,
                err=err.__repr__()
            )
        )

    def run(self):
        self.app.run(
            host='0.0.0.0', port=self.port
        )
