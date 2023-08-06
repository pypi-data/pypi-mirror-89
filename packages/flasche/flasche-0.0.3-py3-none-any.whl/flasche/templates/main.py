from .flasche import flask_setup

# Mandatory to integrate all defined endpoints to api.
# Don't forget to extend the endpoints/__init__.py!
from . import endpoints

# Create flask app object in order to start flask app
app = flask_setup.app

if __name__ == '__main__':
    app.run()
