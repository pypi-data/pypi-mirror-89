import argparse
import configparser
import logging
import os
# import select
# import socket
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

from common.variables import *
from common.my_decorators import log_write
# from server_gui import MainWindow, gui_create_model, HistoryWindow, create_stat_model, ConfigWindow
from server.core import MesProcessor
from server.db_server import ServerStorage
from server.main_window import MainWindow

# import json
# import threading
# import time

log_server = logging.getLogger('server')


# new_connection = False
# conflag_lock = threading.Lock()


@log_write()
def arg_parser():
    '''Функция получения аргументов загрузки сервера'''
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=DEF_PORT, type=int, nargs='?')
    parser.add_argument('-a', default='', nargs='?')
    parser.add_argument('--no_gui', action='store_true')
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p
    gui_flag = namespace.no_gui

    # if not 1023 < listen_port < 65536:
    #     log_server.critical(
    #         f'Попытка запуска сервера с указанием неподходящего порта {listen_port}.
    #         Допустимы адреса с 1024 до 65535.')
    #     sys.exit(1)

    return listen_address, listen_port, gui_flag


@log_write()
def config_load():
    '''Парсер конфигурационного ini файла.'''
    config = configparser.ConfigParser()
    # dir_path = os.path.dirname(os.path.realpath(__file__))
    dir_path = os.getcwd()
    config.read(f"{dir_path}/{'server.ini'}")
    # Если конфиг файл загружен правильно, запускаемся, иначе конфиг по
    # умолчанию.
    if 'SETTINGS' in config:
        return config
    else:
        config.add_section('SETTINGS')
        config.set('SETTINGS', 'default_port', str(DEF_PORT))
        config.set('SETTINGS', 'listen_address', '')
        config.set('SETTINGS', 'database_path', 'db_files/db_server/')
        config.set('SETTINGS', 'database_file', 'server_database.db3')
        return config


def main():
    '''Функция загрузки сервера, получает конфигурацию, аргументы загрузки и стартует главное окно сервера'''
    config = config_load()

    # dir_path = os.path.dirname(os.path.realpath(__file__))
    # config.read(f"{dir_path}/{'server.ini'}")
    database = ServerStorage(os.path.join(config['SETTINGS']['database_path'], config['SETTINGS']['database_file']))
    # database = ServerStorage('db_files/db_server/server_database.db3')

    listen_address, listen_port, gui_flag = arg_parser()
    server = MesProcessor(listen_address, listen_port, database)
    server.daemon = True
    server.start()

    if gui_flag:
        while True:
            command = input('Введите exit для завершения работы сервера.')
            if command == 'exit':
                server.running = False
                server.join()
                break
    else:
        server_app = QApplication(sys.argv)
        server_app.setAttribute(Qt.AA_DisableWindowContextHelpButton)
        main_window = MainWindow(database, server, config)

    # Запускаем GUI
    server_app.exec_()

    server.running = False


if __name__ == '__main__':
    main()
