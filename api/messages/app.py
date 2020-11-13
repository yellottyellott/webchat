import logging
import os

import tornado.gen
import tornado.ioloop
import tornado.iostream
import tornado.web

from . import models
from lib import queue


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
        self.finish('messages api')


class ConversationCollectionHandler(BaseHandler):
    async def get(self):
        data = {'data': await models.get_conversations(self.user['team_id'])}
        self.finish(data)


class ConversationSubscriptionHandler(tornado.web.RequestHandler):
    def set_sse_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header(
            "Access-Control-Allow-Headers",
            "access-control-allow-origin,authorization,content-type")
        self.set_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.set_header('Content-Type', 'text/event-stream')
        self.set_header('Cache-Control', 'no-cache')
        self.set_header('Connection', 'keep-alive')

    async def get(self, conversation_id):
        conversation = await models.get_conversation(conversation_id)
        client_id = self.get_query_argument("channel_uuid")
        self.set_sse_headers()

        async def process_message(message):
            message.enable_async()
            msg = 'data: {}\n\n'.format(message.body.decode('utf8'))
            self.write(msg)
            await self.flush()
            message.finish()

        reader = models.subscribe(
            conversation,
            client_id=client_id,
            callback=process_message)

        try:
            while True:
                await tornado.gen.sleep(1)
        except tornado.iostream.StreamClosedError:
            self.finished = True
        finally:
            reader.close()

    async def options(self):
        self.set_sse_headers()
        self.set_status(204)
        self.finish()


class MessageCollectionHandler(BaseHandler):
    async def post(self, conversation_id):
        conversation = await models.get_conversation(conversation_id)
        data = {
            'conversation_id': conversation['id'],
            'sender': self.user['id'],
            'text': self.get_body_argument("text"),
            'team_id': self.user['team_id']
        }
        await queue.publish('messages', data)
        self.set_status(201)
        self.finish()


class Application(tornado.web.Application):
    def __init__(self, *args, **kwargs):
        routes = [
            (r'^/$', HomeHandler),
            (r'^/api/conversations/(\d+)$', ConversationCollectionHandler),
            (r'^/api/conversations/(\d+)/subscribe$', ConversationSubscriptionHandler),
            (r'^/api/conversations/(\d+)/messages$', MessageCollectionHandler),
        ]
        settings = {
            'template_path': os.path.join(APP_ROOT, 'templates'),
            'debug': True, }
        super().__init__(routes, **settings)


def run(port=8000):
    app = Application()
    loop = tornado.ioloop.IOLoop.current()

    logging.basicConfig(level=logging.DEBUG)
    logging.info("starting server on port {}".format(port))
    app.listen(port)
    loop.start()
