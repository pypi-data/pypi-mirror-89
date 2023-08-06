from flasche import FlaskSetup


APP_NAME = '{{ project }}'
SWAGGER_TITLE = '{{ project }} API'
SWAGGER_DESCRIPTION = 'Show the beauty of Swagger.'
PORT = {{ port }}

flask_setup = FlaskSetup(APP_NAME, PORT)
flask_setup.add_swagger(SWAGGER_TITLE, SWAGGER_DESCRIPTION, url_prefix='/api/')
flask_setup.add_prometheus()
