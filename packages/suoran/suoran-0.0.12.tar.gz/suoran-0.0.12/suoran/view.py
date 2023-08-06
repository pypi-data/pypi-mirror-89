from sanic.response import html
from jinja2 import Environment, FileSystemLoader

environ = None


def init(folder):
    '''
    '''

    global environ
    loader = FileSystemLoader(folder)
    environ = Environment(loader=loader)


def render(path, **data):
    '''
    '''

    global environ
    template = environ.get_template(path)
    result = template.render(**data)
    return html(result)
