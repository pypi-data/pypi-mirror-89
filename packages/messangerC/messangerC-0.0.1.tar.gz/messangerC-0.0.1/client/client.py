import argparse
import logging
import os
import sys

from Crypto.PublicKey import RSA
from PyQt5.QtWidgets import QApplication, QMessageBox

from client.db_client import ClientDatabase
from client.main_window import ClientMainWindow
from client.start_dialog import UserNameDialog
from client.transport import ClientTransport
from common.variables import *
from errors import ServerError
from my_decorators import log_write

log_client = logging.getLogger('client')


# sock_lock = threading.Lock()
# database_lock = threading.Lock()


# @log_write()
# def create_presence(account_name):
#     out = {
#         ACTION: PRESENCE,
#         TIME: time.time(),
#         USER: {
#             ACCOUNT_NAME: account_name
#         }
#     }
#     log_client.debug(f'Сформировано {PRESENCE} сообщение для пользователя {account_name}')
#     return out


# @log_write()
# def process_ans(message):
#     log_client.debug(f'Разбор сообщения от сервера: {message}')
#     if RESPONSE in message:
#         if message[RESPONSE] == 200:
#             return '200 : OK'
#         return f'400 : {message[ERROR]}'
#     raise ValueError


@log_write()
def arg_parser():
    '''Метод для получения аргументов загрузки клиента'''
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEF_IP_ADDRESS, nargs='?')
    parser.add_argument('port', default=DEF_PORT, type=int, nargs='?')
    parser.add_argument('-n', '--name', default=None, nargs='?')
    parser.add_argument('-p', '--password', default='', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port
    client_name = namespace.name
    client_passwd = namespace.password

    if server_port < 1024 or server_port > 65535:
        log_client.critical(
            f'Попытка запуска клиента с неподходящим номером порта: {server_port}. '
            f'Допустимы адреса с 1024 до 65535. Клиент завершается.')
        sys.exit(1)

    return server_address, server_port, client_name, client_passwd


if __name__ == '__main__':
    # main()
    server_address, server_port, client_name, client_passwd = arg_parser()

    # Создаём клиентокое приложение
    client_app = QApplication(sys.argv)

    # Если имя пользователя не было указано в командной строке то запросим его
    start_dialog = UserNameDialog()
    if not client_name or not client_passwd:
        # start_dialog = UserNameDialog()
        client_app.exec_()
        # Если пользователь ввёл имя и нажал ОК, то сохраняем ведённое и
        # удаляем объект, инааче выходим
        if start_dialog.ok_pressed:
            client_name = start_dialog.client_name.text()
            client_passwd = start_dialog.client_passwd.text()
            log_client.debug(f'Using USERNAME = {client_name}, PASSWD = {client_passwd}.')
            # del start_dialog
        else:
            sys.exit(0)

    # Записываем логи
    log_client.info(
        f'Запущен клиент с парамертами: адрес сервера: {server_address} , порт: {server_port}, '
        f'имя пользователя: {client_name}')

    # dir_path = os.path.dirname(os.path.realpath(__file__))
    dir_path = os.getcwd()
    key_file = os.path.join(dir_path, f'{client_name}.key')

    if not os.path.exists(key_file):
        keys = RSA.generate(2048, os.urandom)
        with open(key_file, 'wb') as key:
            key.write(keys.export_key())
    else:
        with open(key_file, 'rb') as key:
            keys = RSA.import_key(key.read())

    log_client.debug("Keys sucsessfully loaded.")
    # Создаём объект базы данных
    database = ClientDatabase(client_name)
    # print(client_name)

    # Создаём объект - транспорт и запускаем транспортный поток
    try:
        transport = ClientTransport(
            server_port,
            server_address,
            database,
            client_name,
            client_passwd,
            keys)
    except ServerError as error:
        message = QMessageBox()
        message.critical(start_dialog, 'Ошибка сервера', error.text)
        sys.exit(1)

    transport.setDaemon(True)
    transport.start()

    del start_dialog
    # Создаём GUI
    main_window = ClientMainWindow(database, transport, keys)
    main_window.make_connection(transport)
    main_window.setWindowTitle(f'Чат Программа alpha release - {client_name}')
    client_app.exec_()

    # графическая оболочка закрыта, закрываем транспорт
    transport.transport_shutdown()
    transport.join()
