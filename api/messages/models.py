import nsq


async def get_conversations(team_id):
    conversations = [{
        "id": 123,
        "team_id": 123,
        "created_at": "2020-11-01T06:00:00.123",
    }]
    return conversations


async def get_conversation(id):
    conversation = {
        "id": 123,
        "team_id": 123,
        "created_at": "2020-11-01T06:00:00.123",
    }
    return conversation


async def get_messages(conversation_id):
    messages = [{
        "created_at": "2020-11-01T09:00:00.100",
        "text": "Hello, just had a few questions.",
        "sender": "george"
    }]
    return messages


def subscribe(conversation, client_id, callback):
    reader = nsq.Reader(
        message_handler=callback,
        lookupd_http_addresses=['http://nsqlookupd:4161'],
        topic='conversations.{}'.format(conversation['id']),
        channel='web-{}#ephemeral'.format(client_id),
        max_in_flight=10)
    return reader
