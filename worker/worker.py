import json
import logging

import nsq
import tornado.httpclient

from lib import queue


def route(data):
    topic = 'conversations.{}'.format(data['conversation_id'])
    return topic


async def callback(message):
    """Route message from firehose to conversation topic."""
    try:
        data = json.loads(message.body)
        logging.debug(message.body)
        topic = route(data)
        # save to db
        await queue.publish(topic, data)
    except tornado.httpclient.HTTPClientError as err:
        logging.error("request failed: {}".format(err.response.body))
        message.requeue()
    except Exception:
        logging.exception("error procesing message")
        message.finish()
    else:
        message.finish()


def run():
    nsq.Reader(
        message_handler=callback,
        lookupd_http_addresses=['http://nsqlookupd:4161'],
        topic='messages',
        channel='worker',
        max_in_flight=10)
    nsq.run()
