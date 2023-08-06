from os.path import dirname, abspath
from jinja2 import Environment, FileSystemLoader, select_autoescape
from functools import wraps

__env = None


def setup_jinja(path):
    global __env
    __env = Environment(loader=FileSystemLoader(path),
                        autoescape=select_autoescape(['html', 'xml']))


def jinja(path):
    def render(func):
        try:
            template = __env.get_template(path)

            def handler(request, response, *args):
                response.content_type = 'text/html'
                response.response_encoding = 'utf-8'
                params = func(request, response, *args)
                if not response.location:
                    body = template.render(**params)
                    body = response.encode_response(body)
                else:
                    body = params
                return body

            return handler
        except:
            return func
    return render
