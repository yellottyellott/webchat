import json

import tornado.httpclient


async def publish(topic, data):
    client = tornado.httpclient.AsyncHTTPClient()
    url = 'http://nsqd:4151/pub?topic={}'.format(topic)
    response = await client.fetch(url, method='POST', body=json.dumps(data))
    return response
