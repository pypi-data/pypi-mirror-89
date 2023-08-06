import os
from shutil import copy, copytree
from jinja2 import Environment, FileSystemLoader, select_autoescape


class ProjectBuilder:
    def __init__(self, project, port):
        self.project = project
        self.port = port
        self.template_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'templates'
        )
        self.env = Environment(
            loader=FileSystemLoader(self.template_path),
            autoescape=select_autoescape(['py'])
        )

    def create_src_dst(self, path):
        src = os.path.join(self.template_path, path)
        dst = os.path.join(self.project, path)
        return src, dst

    def copy_main_py(self):
        src, dst = self.create_src_dst('main.py')
        copy(src, dst)

    def copy_endpoints(self):
        src, dst = self.create_src_dst('endpoints')
        copytree(src, dst)

    def create_init_py(self):
        filepath = os.path.join(self.project, '__init__.py')
        open(filepath, 'a').close()

    def create_flasche_py(self):
        values = {
            'project': self.project,
            'port': self.port
        }
        src, dst = self.create_src_dst('flasche.py')
        output = self.render_file('flasche.py', values)

        with open(dst, 'w') as f:
            f.write(output)

    def render_file(self, file, values):
        template = self.env.get_template(file)
        return template.render(**values)

    def make_project_folder(self):
        try:
            os.mkdir(self.project)
        except FileExistsError as e:
            print('Failed to build project.')
            print('Project folder {dst} does already exist.'.format(dst=self.project))
            print('The project folder must not exist before.')
            raise e

    def build(self):
        self.make_project_folder()
        self.copy_main_py()
        self.copy_endpoints()
        self.create_init_py()
        self.create_flasche_py()
