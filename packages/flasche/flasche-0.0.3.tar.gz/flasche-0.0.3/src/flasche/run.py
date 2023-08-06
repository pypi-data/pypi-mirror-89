import os


class ProjectRunner:
    def __init__(self, project):
        self.project = project

    def run(self):
        flask_app = os.path.join(self.project, 'main.py')
        os.environ['FLASK_APP'] = flask_app
        os.system('flask run')
        os.unsetenv('FLASK_APP')
