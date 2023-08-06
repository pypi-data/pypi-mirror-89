import unittest

from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, PRESENCE, TIME, USER, ERROR
from server.core import MesProcessor


class TestMyServer(unittest.TestCase):
    def test_process_client_message_correctquery(self):
        mass = {
            ACTION: PRESENCE,
            TIME: 1.1,
            USER: {
                ACCOUNT_NAME: "Guest"
            },
        }
        self.assertEqual(MesProcessor.process_client_message(mass), {RESPONSE: 200})

    def test_process_client_message_invalidtime(self):
        mass = {
            ACTION: PRESENCE,
            USER: {
                ACCOUNT_NAME: "Guest"
            },
        }
        self.assertNotEqual(MesProcessor.process_client_message(mass), {RESPONSE: 200})

    def test_process_client_message_invalidname(self):
        mass = {
            ACTION: PRESENCE,
            TIME: 1.1,
            USER: {
                ACCOUNT_NAME: ""
            },
        }
        self.assertNotEqual(MesProcessor.process_client_message(mass), {RESPONSE: 200})

    def test_process_client_message_invalid_action_name(self):
        mass = {
            ACTION: "One",
            TIME: 1.1,
            USER: {
                ACCOUNT_NAME: "Guest",
            },
        }
        self.assertEqual(MesProcessor.process_client_message(mass), {RESPONSE: 400, ERROR: 'Bad Request'})

    def test_process_client_message_invalid_action(self):
        mass = {
            TIME: 1.1,
            USER: {
                ACCOUNT_NAME: "Guest",
            },
        }
        self.assertEqual(MesProcessor.process_client_message(mass), {RESPONSE: 400, ERROR: 'Bad Request'})


# {RESPONSE: 400, ERROR: 'Bad Request'}
if __name__ == '__main__':
    unittest.main()
