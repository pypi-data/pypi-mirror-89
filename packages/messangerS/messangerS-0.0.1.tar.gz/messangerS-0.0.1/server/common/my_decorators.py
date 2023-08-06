import logging
import socket
import sys
import traceback
from functools import wraps

sys.path.append('../')

if sys.argv[0].find("server") > -1:
    log_module = logging.getLogger('server')
else:
    log_module = logging.getLogger('client')


class log_write():
    '''Класс декоратор записи логов работы функции'''

    def __call__(self, funct, *args, **kwargs):
        @wraps(funct)
        def decor(*args, **kwargs):
            rez = funct(*args, **kwargs)
            # "<дата-время> Функция func_z() вызвана из функции main"
            log_module.debug(
                f'Функция {funct.__name__} вызвана из функции {traceback.format_stack()[0].strip().split()[-1]}'
                f' в модуле {funct.__module__} с параметрами: {args}, {kwargs}', stacklevel=2)
            return rez

        return decor


def login_required(func):
    '''
    Декоратор, проверяющий, что клиент авторизован на сервере.
    Проверяет, что передаваемый объект сокета находится в
    списке авторизованных клиентов.
    За исключением передачи словаря-запроса
    на авторизацию. Если клиент не авторизован,
    генерирует исключение TypeError
    '''

    def checker(*args, **kwargs):
        # проверяем, что первый аргумент - экземпляр MessageProcessor
        # Импортить необходимо тут, иначе ошибка рекурсивного импорта.
        from server.core import MesProcessor
        from common.variables import ACTION, PRESENCE
        if isinstance(args[0], MesProcessor):
            found = False
            for arg in args:
                if isinstance(arg, socket.socket):
                    # Проверяем, что данный сокет есть в списке names класса
                    # MessageProcessor
                    for client in args[0].names:
                        if args[0].names[client] == arg:
                            found = True

            # Теперь надо проверить, что передаваемые аргументы не presence
            # сообщение. Если presense, то разрешаем
            for arg in args:
                if isinstance(arg, dict):
                    if ACTION in arg and arg[ACTION] == PRESENCE:
                        found = True
            # Если не не авторизован и не сообщение начала авторизации, то
            # вызываем исключение.
            if not found:
                raise TypeError
        return func(*args, **kwargs)

    return checker
