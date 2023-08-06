DEF_PORT = 7777
DEF_IP_ADDRESS = '127.0.0.1'
MAX_CONNECTIONS = 15
MAX_PACKAGE_LENGTH = 16392
ENCODING = 'utf-8'
DATABASE_SERVER = 'sqlite:///db_files/db_server/server_database.db3'
DATABASE_CLIENT = 'sqlite:///db_files/db_client/client_'
SERVER_CONFIG = 'server.ini'

# Ключи протокола (основные)
ACTION = 'action'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'
SENDER = 'sender'
DESTINATION = 'to'
DATA = 'bin'
PUBLIC_KEY = 'pubkey'

# Доп. ключи протокола
PRESENCE = 'presence'
RESPONSE = 'response'
ERROR = 'error'
MESSAGE = 'message'
TEXT_MESSAGE = 'text_message'
EXIT = 'exit'
GET_CONTACTS = 'get_contacts'
LIST_INFO = 'data_list'
REMOVE_CONTACT = 'remove'
ADD_CONTACT = 'add'
USERS_REQUEST = 'get_users'
PUBLIC_KEY_REQUEST = 'pubkey_need'

RESPONSE_200 = {RESPONSE: 200}
RESPONSE_400 = {
    RESPONSE: 400,
    ERROR: 'Bad request'
}
RESPONSE_202 = {RESPONSE: 202,
                LIST_INFO: None
                }

RESPONSE_511 = {
    RESPONSE: 511,
    DATA: None
}

RESPONSE_205 = {
    RESPONSE: 205
}
