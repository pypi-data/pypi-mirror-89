import json
import sys

sys.path.append('../')

from common.variables import *


def get_mes(client):
    '''Метод получает сообщение от клиента'''
    encoded_response = client.recv(MAX_PACKAGE_LENGTH)
    # encoded_response = client.received(MAX_PACKAGE_LENGTH)
    # enc = client.recv['encoding']
    if isinstance(encoded_response, bytes):
        json_response = encoded_response.decode(ENCODING)
        response = json.loads(json_response)
        if isinstance(response, dict):
            return response
        raise ValueError
    raise ValueError


def send_mes(sock, message):
    '''Метод отправки сообщения'''
    js_message = json.dumps(message)
    encoded_message = js_message.encode(ENCODING)
    sock.send(encoded_message)
