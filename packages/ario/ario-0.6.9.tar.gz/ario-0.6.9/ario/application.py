from werkzeug.wrappers import Request, Response


class Application:
    def __init__(self, controller):
        if controller is not None:
            self.controller = controller

    def __call__(self, environ, start_response):
        response = self.controller(environ, start_response)
        return response

