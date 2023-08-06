import datetime

from sqlalchemy.sql import default_comparator
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import mapper, sessionmaker

from common.variables import DATABASE_SERVER


class ServerStorage:
    '''
   Класс - оболочка для работы с базой данных сервера.
   Использует SQLite базу данных, реализован с помощью
   SQLAlchemy ORM и используется классический подход.
   '''

    class UsersEntireList:
        '''Класс - отображение таблицы всех пользователей.'''

        def __init__(self, login_name, passwd_hash):
            self.login_name = login_name
            self.entry_time = datetime.datetime.now()
            self.passwd_hash = passwd_hash
            self.pubkey = None
            self.id = None

    class ActiveUsers:
        '''Класс - отображение таблицы активных пользователей.'''

        def __init__(self, user_id, user_ip, user_port, time_login):
            self.user = user_id
            self.ip = user_ip
            self.port = user_port
            self.time_login = time_login
            self.id = None

    class HistoryLogin:
        '''Класс - отображение таблицы истории входов.'''

        def __init__(self, user_name, user_ip, user_port, time_login):
            self.name = user_name
            self.ip = user_ip
            self.port = user_port
            self.time_login = time_login
            self.id = None

    class UsersContacts:
        '''Класс - отображение таблицы контактов пользователей.'''

        def __init__(self, user_id, contact):
            self.id = None
            self.user = user_id
            self.contact_user = contact

    class UsersHistoryMessage:
        '''Класс - отображение таблицы истории действий.'''

        def __init__(self, user_name):
            self.id = None
            self.user = user_name
            self.send = 0
            self.received = 0

    def __init__(self, path):
        print(path)
        self.database_engine = create_engine(DATABASE_SERVER, echo=False, pool_recycle=7200,
                                             connect_args={'check_same_thread': False})
        # self.database_engine = create_engine(DATABASE_SERVER, echo=False, pool_recycle=7200)
        self.metadata = MetaData()

        users = Table('Users', self.metadata,
                      Column('id', Integer, primary_key=True),
                      Column('login_name', String, unique=True),
                      Column('entry_time', DateTime),
                      Column('passwd_hash', String),
                      Column('pubkey', Text)
                      )

        users_active = Table('Users_active', self.metadata,
                             Column('id', Integer, primary_key=True),
                             Column('ip', String),
                             Column('port', Integer),
                             Column('time_login', DateTime),
                             Column('user', ForeignKey('Users.id'), unique=True)
                             )

        users_history_login = Table('Users_history_login', self.metadata,
                                    Column('name', ForeignKey('Users.id')),
                                    Column('ip', String),
                                    Column('port', Integer),
                                    Column('time_login', DateTime),
                                    Column('id', Integer, primary_key=True)
                                    )

        user_contacts = Table('User_contacts', self.metadata,
                              Column('id', Integer, primary_key=True),
                              Column('user', ForeignKey('Users.id')),
                              Column('contact_user', ForeignKey('Users.id'))
                              )

        user_history_message = Table('User_history_message', self.metadata,
                                     Column('id', Integer, primary_key=True),
                                     Column('user', ForeignKey('Users.id')),
                                     Column('send', Integer, default=0),
                                     Column('received', Integer, default=0)
                                     )

        self.metadata.create_all(self.database_engine)

        mapper(self.UsersEntireList, users)
        mapper(self.ActiveUsers, users_active)
        mapper(self.HistoryLogin, users_history_login)
        mapper(self.UsersContacts, user_contacts)
        mapper(self.UsersHistoryMessage, user_history_message)

        Session = sessionmaker(bind=self.database_engine)
        self.session = Session()

        self.session.query(self.ActiveUsers).delete()
        self.session.commit()

    def login_user(self, username, ip, port, key):
        '''
        Метод выполняющийся при входе пользователя, записывает в базу факт входа
        Обновляет открытый ключ пользователя при его изменении.
        '''
        print(username, ip, port)
        user_in_base = self.session.query(self.UsersEntireList).filter_by(login_name=username)
        if user_in_base.count():
            user = user_in_base.first()
            user.entry_time = datetime.datetime.now()
            if user.pubkey != key:
                user.pubkey = key
            # Если нету, то генерируем исключение
        else:
            raise ValueError('Пользователь не зарегистрирован.')
        # if user_in_base.count():
        #     user = user_in_base.first()
        #     user.entry_time = datetime.datetime.now()
        # else:
        #     user = self.UsersEntireList(username)
        #     self.session.add(user)
        #     self.session.commit()
        #     user_in_history = self.UsersHistoryMessage(user.id)
        #     self.session.add(user_in_history)

        active_user_new = self.ActiveUsers(user.id, ip, port, datetime.datetime.now())
        self.session.add(active_user_new)

        user_history_login = self.HistoryLogin(user.id, ip, port, datetime.datetime.now())
        self.session.add(user_history_login)
        self.session.commit()

    def logout_user(self, username):
        '''Метод фиксирующий отключения пользователя.'''
        user_in_base = self.session.query(self.UsersEntireList).filter_by(login_name=username).first()
        self.session.query(self.ActiveUsers).filter_by(user=user_in_base.id).delete()
        self.session.commit()

    def all_users_list(self):
        '''Метод возвращающий список известных пользователей со временем последнего входа.'''
        query = self.session.query(
            self.UsersEntireList.login_name,
            # self.UsersEntireList.login_name,
            self.UsersEntireList.entry_time
        )
        return query.all()

    def active_users_list(self):
        '''Метод возвращающий список активных пользователей.'''
        query = self.session.query(
            self.UsersEntireList.login_name,
            self.ActiveUsers.ip,
            self.ActiveUsers.port,
            self.ActiveUsers.time_login
        ).join(self.UsersEntireList)
        return query.all()

    def login_history_all_or_username(self, username=None):
        '''Метод возвращающий историю входов всех пользователей или конкретного пользователя'''
        query = self.session.query(self.UsersEntireList.login_name,
                                   self.HistoryLogin.time_login,
                                   self.HistoryLogin.ip,
                                   self.HistoryLogin.port
                                   ).join(self.UsersEntireList)
        if username:
            query = query.filter(self.UsersEntireList.login_name == username)
        return query.all()

    def process_message(self, sender, recipient):
        '''Метод записывающий в таблицу статистики факт передачи сообщения.'''
        sender1 = self.session.query(self.UsersEntireList).filter_by(login_name=sender).first().id
        recipient1 = self.session.query(self.UsersEntireList).filter_by(login_name=recipient).first().id
        sender_row = self.session.query(self.UsersHistoryMessage).filter_by(user=sender1).first()
        recipient_row = self.session.query(self.UsersHistoryMessage).filter_by(user=recipient1).first()
        sender_row.send += 1
        recipient_row.received += 1
        # if recipient_row:
        #     recipient_row.received += 1
        # else:
        #     user = self.UsersHistoryMessage(recipient)
        #     self.session.add(user)
        #     self.session.commit()
        #     user.received += 1
        #
        # if sender_row:
        #     sender_row.send += 1
        # else:
        #     user = self.UsersHistoryMessage(sender)
        #     self.session.add(user)
        #     self.session.commit()
        #     user.send += 1
        self.session.commit()

    def get_process_message(self):
        '''Метод возвращающий статистику сообщений.'''
        query = self.session.query(
            self.UsersEntireList.login_name,
            self.UsersHistoryMessage.send,
            self.UsersHistoryMessage.received,
        ).join(self.UsersEntireList)
        return query.all()

    def add_contact(self, user, contact):
        '''Метод добавления контакта для пользователя.'''
        user = self.session.query(self.UsersEntireList).filter_by(login_name=user).first()
        contact = self.session.query(self.UsersEntireList).filter_by(login_name=contact).first()

        if not contact or self.session.query(self.UsersContacts).filter_by(user=user.id,
                                                                           contact_user=contact.id).count():
            return

        contact_row = self.UsersContacts(user.id, contact.id)
        self.session.add(contact_row)
        self.session.commit()

    def get_users_contact(self, log_user=None):
        '''Метод возвращающий список контактов пользователя.'''
        # user = self.session.query(self.UsersEntireList).filter_by(login_name=user).first()
        query = self.session.query(
            self.UsersContacts.contact_user,
            self.UsersEntireList.login_name,
            self.UsersContacts.user,
        ).join(self.UsersEntireList, self.UsersEntireList.id == self.UsersContacts.contact_user)
        if log_user:
            user1 = self.session.query(self.UsersEntireList).filter_by(login_name=log_user).first()
            query = query.filter(self.UsersContacts.user == user1.id)
            return [contact[1] for contact in query.all()]
        else:
            return query.all()

    def remove_contact(self, user, contact_user):
        '''Метод удаления контакта пользователя.'''
        user = self.session.query(self.UsersEntireList).filter_by(login_name=user).first()
        contact = self.session.query(self.UsersEntireList).filter_by(login_name=contact_user).first()

        if not contact:
            return

        self.session.query(self.UsersContacts).filter(
            self.UsersContacts.user == user.id,
            self.UsersContacts.contact_user == contact.id
        ).delete()
        self.session.commit()

    def add_user(self, name, passwd_hash):
        '''
        Метод регистрации пользователя.
        Принимает имя и хэш пароля, создаёт запись в таблице статистики.
        '''
        user_row = self.UsersEntireList(name, passwd_hash)
        self.session.add(user_row)
        self.session.commit()
        history_row = self.UsersHistoryMessage(user_row.id)
        self.session.add(history_row)
        self.session.commit()

    def remove_user(self, name):
        '''Метод удаляющий пользователя из базы.'''
        user = self.session.query(self.UsersEntireList).filter_by(login_name=name).first()
        self.session.query(self.ActiveUsers).filter_by(user=user.id).delete()
        self.session.query(self.HistoryLogin).filter_by(name=user.id).delete()
        self.session.query(self.UsersContacts).filter_by(user=user.id).delete()
        self.session.query(
            self.UsersContacts).filter_by(
            contact=user.id).delete()
        self.session.query(self.UsersHistoryMessage).filter_by(user=user.id).delete()
        self.session.query(self.UsersEntireList).filter_by(login_name=name).delete()
        self.session.commit()

    def get_hash(self, name):
        '''Метод получения хэша пароля пользователя.'''
        user = self.session.query(self.UsersEntireList).filter_by(login_name=name).first()
        return user.passwd_hash

    def get_pubkey(self, name):
        '''Метод получения публичного ключа пользователя.'''
        user = self.session.query(self.UsersEntireList).filter_by(login_name=name).first()
        return user.pubkey

    def check_user(self, name):
        '''Метод проверяющий существование пользователя.'''
        if self.session.query(self.UsersEntireList).filter_by(login_name=name).count():
            return True
        else:
            return False


if __name__ == '__main__':
    test_db = ServerStorage('db_files/db_server/server_database.db3')
    test_db.login_user(username='user_1', ip='192.168.1.4', port=8888)
    test_db.login_user(username='user_2', ip='192.168.1.5', port=7777)
    test_db.login_user(username='user_5', ip='192.168.1.3', port=7755)
    test_db.login_user(username='user_3', ip='192.168.9.3', port=5666)
    test_db.login_user(username='user_4', ip='192.165.9.3', port=5366)
    test_db.login_user(username='user_6', ip='192.164.9.3', port=5266)
    print(test_db.active_users_list())
    test_db.logout_user(username='user_1')
    print(test_db.active_users_list())
    test_db.login_history_all_or_username(username='user_1')
    print(test_db.all_users_list())
    test_db.process_message(sender='user_6', recipient='user_3')
    print(test_db.get_process_message())
    test_db.add_contact(user='user_5', contact='user_2')
    test_db.add_contact(user='user_5', contact='user_3')
    test_db.add_contact(user='user_5', contact='user_4')
    test_db.add_contact(user='user_4', contact='user_3')
    print(test_db.get_users_contact('user_5'))
    print(test_db.get_users_contact())
    test_db.remove_contact(user='user_5', contact_user='user_3')
    print(test_db.get_users_contact('df'))
