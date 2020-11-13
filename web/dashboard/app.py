import logging
import os
import uuid

import tornado.ioloop
import tornado.web


APP_ROOT = os.path.abspath(os.path.dirname(__file__))


class BaseHandler(tornado.web.RequestHandler):
    def prepare(self, *args, **kwargs):
        super().prepare(*args, **kwargs)
        self.user = {
            "id": 123,
            "username": "fauci",
            "team_id": 123
        }


class HomeHandler(BaseHandler):
    async def get(self):
        self.render('index.html', channel_uuid=uuid.uuid4())


class Application(tornado.web.Application):
    def __init__(self, *args, **kwargs):
        routes = [
            (r'^/$', HomeHandler),
        ]
        settings = {
            'template_path': os.path.join(APP_ROOT, 'templates'),
            'debug': True, }
        super().__init__(routes, **settings)


def run(port=8001):
    app = Application()
    loop = tornado.ioloop.IOLoop.current()

    logging.info("starting server on port {}".format(port))
    app.listen(port)
    loop.start()
