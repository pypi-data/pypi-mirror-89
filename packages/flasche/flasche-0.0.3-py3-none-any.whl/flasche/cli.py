import click

from .build import ProjectBuilder
from .run import ProjectRunner


@click.group()
def main():
    pass


@main.command()
@click.argument('project')
@click.option('-p', '--port', default=8000)
def build(project, port):
    click.echo("build project {p}...".format(p=project))
    builder = ProjectBuilder(project, port)
    builder.build()
    click.echo("...done")
    click.echo("run the app by \"flasche run {p}\"".format(p=project))


@main.command()
@click.argument('project')
def run(project):
    click.echo("run project {p}".format(p=project))
    runner = ProjectRunner(project)
    runner.run()
