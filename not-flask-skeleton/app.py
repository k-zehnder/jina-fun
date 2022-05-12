# https://ains.co/blog/things-which-arent-magic-flask-part-1.html
# KZ 4-7-22

from functools import wraps
from abc import ABC, abstractmethod


class NotFlask(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def route(self):
        pass

    @abstractmethod
    def serve(self):
        pass


class NotFlaskTry(NotFlask):
    def __init__(self):
        self.routes = {}

    def route(self, route_str):
        def decorator(f):
            self.routes[route_str] = f
            return f
        return decorator

    def serve(self, path):  # sourcery skip: use-named-expression
        view_function = self.routes.get(path)
        if view_function:
            return view_function()
        else:
            raise ValueError(f"route {path} not registered.")
        

if __name__ == "__main__":
    app = NotFlaskTry()

    @app.route("/index")
    def index():
        return "[INFO] running index."

    @app.route("/search")
    def search():
        return "[INFO] running search."

    print(app.serve("/index"))
    print(app.serve("/search"))

