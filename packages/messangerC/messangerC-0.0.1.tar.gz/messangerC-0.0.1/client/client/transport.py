import binascii
import hashlib
import hmac
import logging
import socket
import sys
import threading
import time

from PyQt5.QtCore import QObject, pyqtSignal

sys.path.append('../')
from common.utils import *
from common.variables import *
from common.errors import ServerError

# Логер и объект блокировки для работы с сокетом.
log_client = logging.getLogger('client')
socket_lock = threading.Lock()


# Класс - Траннспорт, отвечает за взаимодействие с сервером
class ClientTransport(threading.Thread, QObject):
    '''Класс взаимодействия клиента с сервером'''
    # Сигналы новое сообщение и потеря соединения
    new_message = pyqtSignal(dict)
    # new_message = pyqtSignal()
    message_205 = pyqtSignal()
    connection_lost = pyqtSignal()

    def __init__(self, port, ip_address, database, username, passwd, keys):
        # Вызываем конструктор предка
        threading.Thread.__init__(self)
        QObject.__init__(self)

        # Класс База данных - работа с базой
        self.database = database
        # Имя пользователя
        self.username = username
        # пароль и ключ
        self.password = passwd
        self.keys = keys
        # Сокет для работы с сервером
        self.transport = None
        # Устанавливаем соединение:
        self.connection_init(port, ip_address)
        # Обновляем таблицы известных пользователей и контактов
        try:
            self.user_list_update()
            self.contacts_list_update()
        except OSError as err:
            if err.errno:
                log_client.critical(f'Потеряно соединение с сервером.')
                raise ServerError('Потеряно соединение с сервером!')
            log_client.error('Timeout соединения при обновлении списков пользователей.')
        except json.JSONDecodeError:
            log_client.critical(f'Потеряно соединение с сервером.')
            raise ServerError('Потеряно соединение с сервером!')
            # Флаг продолжения работы транспорта.
        self.running = True

    # Функция инициализации соединения с сервером
    def connection_init(self, port, ip):
        '''Метод отвечающий за устанновку соединения с сервером.'''
        # Инициализация сокета и сообщение серверу о нашем появлении
        self.transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Таймаут необходим для освобождения сокета.
        self.transport.settimeout(5)

        # Соединяемся, 5 попыток соединения, флаг успеха ставим в True если удалось
        connected = False
        for i in range(5):
            log_client.info(f'Попытка подключения №{i + 1}')
            try:
                self.transport.connect((ip, port))
            except (OSError, ConnectionRefusedError):
                pass
            else:
                connected = True
                break
            time.sleep(1)

        # Если соединится не удалось - исключение
        if not connected:
            log_client.critical('Не удалось установить соединение с сервером')
            raise ServerError('Не удалось установить соединение с сервером')

        log_client.debug('Установлено соединение с сервером')

        # Запускаем процедуру авторизации
        # Получаем хэш пароля
        passwd_bytes = self.password.encode('utf-8')
        salt = self.username.lower().encode('utf-8')
        passwd_hash = hashlib.pbkdf2_hmac('sha512', passwd_bytes, salt, 10000)
        passwd_hash_string = binascii.hexlify(passwd_hash)

        log_client.debug(f'Passwd hash ready: {passwd_hash_string}')

        # Получаем публичный ключ и декодируем его из байтов
        pubkey = self.keys.publickey().export_key().decode('ascii')

        # Авторизируемся на сервере
        with socket_lock:
            presense = {
                ACTION: PRESENCE,
                TIME: time.time(),
                USER: {
                    ACCOUNT_NAME: self.username,
                    PUBLIC_KEY: pubkey
                }
            }
            log_client.debug(f"Presense message = {presense}")
            # Отправляем серверу приветственное сообщение.
            try:
                send_mes(self.transport, presense)
                ans = get_mes(self.transport)
                log_client.debug(f'Server response = {ans}.')
                # Если сервер вернул ошибку, бросаем исключение.
                if RESPONSE in ans:
                    if ans[RESPONSE] == 400:
                        raise ServerError(ans[ERROR])
                    elif ans[RESPONSE] == 511:
                        # Если всё нормально, то продолжаем процедуру
                        # авторизации.
                        ans_data = ans[DATA]
                        hash = hmac.new(passwd_hash_string, ans_data.encode('utf-8'), 'MD5')
                        digest = hash.digest()
                        my_ans = RESPONSE_511
                        my_ans[DATA] = binascii.b2a_base64(
                            digest).decode('ascii')
                        send_mes(self.transport, my_ans)
                        self.process_server_ans(get_mes(self.transport))
            except (OSError, json.JSONDecodeError) as err:
                log_client.debug(f'Connection error.', exc_info=err)
                raise ServerError('Сбой соединения в процессе авторизации.')

        # Посылаем серверу приветственное сообщение и получаем ответ что всё нормально или ловим исключение.

    #     try:
    #         with socket_lock:
    #             send_mes(self.transport, self.create_presence())
    #             self.process_server_ans(get_mes(self.transport))
    #     except (OSError, json.JSONDecodeError):
    #         logger.critical('Потеряно соединение с сервером!')
    #         raise ServerError('Потеряно соединение с сервером!')
    #
    #     # Раз всё хорошо, сообщение о установке соединения.
    #     logger.info('Соединение с сервером успешно установлено.')
    #
    # # Функция, генерирующая приветственное сообщение для сервера
    # def create_presence(self):
    #     out = {
    #         ACTION: PRESENCE,
    #         TIME: time.time(),
    #         USER: {
    #             ACCOUNT_NAME: self.username
    #         }
    #     }
    #     logger.debug(f'Сформировано {PRESENCE} сообщение для пользователя {self.username}')
    #     return out

    # Функция обрабатывающяя сообщения от сервера. Ничего не возращает. Генерирует исключение при ошибке.
    def process_server_ans(self, message):
        '''Метод обработчик поступающих сообщений с сервера.'''
        log_client.debug(f'Разбор сообщения от сервера: {message}')

        # Если это подтверждение чего-либо
        if RESPONSE in message:
            if message[RESPONSE] == 200:
                return
            elif message[RESPONSE] == 400:
                raise ServerError(f'{message[ERROR]}')
            elif message[RESPONSE] == 205:
                self.user_list_update()
                self.contacts_list_update()
                self.message_205.emit()
            else:
                log_client.debug(f'Принят неизвестный код подтверждения {message[RESPONSE]}')

        # Если это сообщение от пользователя добавляем в базу, даём сигнал о новом сообщении
        elif ACTION in message and message[ACTION] == MESSAGE and SENDER in message and DESTINATION in message \
                and TEXT_MESSAGE in message and message[DESTINATION] == self.username:
            log_client.debug(
                f'Получено сообщение от пользователя {message[SENDER]}:{message[TEXT_MESSAGE]}')
            self.new_message.emit(message)
            # # log_client.debug(f'Получено сообщение от пользователя {message[SENDER]}:{message[TEXT_MESSAGE]}')
            # self.database.save_message(message[SENDER], 'in', message[TEXT_MESSAGE])
            # log_client.debug(f'Получено сообщение от пользователя {message[SENDER]}: {message[TEXT_MESSAGE]}')
            # # self.new_message.emit(message[SENDER])
            # self.new_message.emit(message)
            # # self.new_message.emit()

    # Функция обновляющая контакт - лист с сервера
    def contacts_list_update(self):
        '''Метод обновляющий с сервера список контактов.'''
        self.database.contacts_clear()
        log_client.debug(f'Запрос контакт листа для пользователся {self.name}')
        req = {
            ACTION: GET_CONTACTS,
            TIME: time.time(),
            USER: self.username
        }
        log_client.debug(f'Сформирован запрос {req}')
        with socket_lock:
            send_mes(self.transport, req)
            ans = get_mes(self.transport)
        log_client.debug(f'Получен ответ {ans}')
        if RESPONSE in ans and ans[RESPONSE] == 202:
            for contact in ans[LIST_INFO]:
                self.database.add_contact(contact)
        else:
            log_client.error('Не удалось обновить список контактов.')

    # Функция обновления таблицы известных пользователей.
    def user_list_update(self):
        '''Метод обновляющий с сервера список пользователей.'''
        log_client.debug(f'Запрос списка известных пользователей {self.username}')
        req = {
            ACTION: USERS_REQUEST,
            TIME: time.time(),
            ACCOUNT_NAME: self.username
        }
        with socket_lock:
            send_mes(self.transport, req)
            ans = get_mes(self.transport)
        if RESPONSE in ans and ans[RESPONSE] == 202:
            self.database.add_users(ans[LIST_INFO])
        else:
            log_client.error('Не удалось обновить список известных пользователей.')

    def key_request(self, user):
        '''Метод запрашивающий с сервера публичный ключ пользователя.'''
        log_client.debug(f'Запрос публичного ключа для {user}')
        req = {
            ACTION: PUBLIC_KEY_REQUEST,
            TIME: time.time(),
            ACCOUNT_NAME: user
        }
        with socket_lock:
            send_mes(self.transport, req)
            ans = get_mes(self.transport)
        if RESPONSE in ans and ans[RESPONSE] == 511:
            return ans[DATA]
        else:
            log_client.error(f'Не удалось получить ключ собеседника{user}.')

    # Функция сообщающая на сервер о добавлении нового контакта
    def add_contact(self, contact):
        '''Метод отправляющий на сервер сведения о добавлении контакта.'''
        log_client.debug(f'Создание контакта {contact}')
        req = {
            ACTION: ADD_CONTACT,
            TIME: time.time(),
            USER: self.username,
            ACCOUNT_NAME: contact
        }
        with socket_lock:
            send_mes(self.transport, req)
            self.process_server_ans(get_mes(self.transport))

    # Функция удаления клиента на сервере
    def remove_contact(self, contact):
        '''Метод отправляющий на сервер сведения о удалении контакта.'''
        log_client.debug(f'Удаление контакта {contact}')
        req = {
            ACTION: REMOVE_CONTACT,
            TIME: time.time(),
            USER: self.username,
            ACCOUNT_NAME: contact
        }
        with socket_lock:
            send_mes(self.transport, req)
            self.process_server_ans(get_mes(self.transport))

    # Функция закрытия соединения, отправляет сообщение о выходе.
    def transport_shutdown(self):
        '''Метод уведомляющий сервер о завершении работы клиента.'''
        self.running = False
        message = {
            ACTION: EXIT,
            TIME: time.time(),
            ACCOUNT_NAME: self.username
        }
        with socket_lock:
            try:
                send_mes(self.transport, message)
            except OSError:
                pass
        log_client.debug('Транспорт завершает работу.')
        time.sleep(0.5)

    # Функция отправки сообщения на сервер
    def send_message(self, to, message):
        '''Метод отправляющий на сервер сообщения для пользователя.'''
        message_dict = {
            ACTION: MESSAGE,
            SENDER: self.username,
            DESTINATION: to,
            TIME: time.time(),
            TEXT_MESSAGE: message
        }
        log_client.debug(f'Сформирован словарь сообщения: {message_dict}')

        # Необходимо дождаться освобождения сокета для отправки сообщения
        with socket_lock:
            send_mes(self.transport, message_dict)
            self.process_server_ans(get_mes(self.transport))
            log_client.info(f'Отправлено сообщение для пользователя {to}')

    def run(self):
        '''Метод содержащий основной цикл работы транспортного потока.'''
        log_client.debug('Запущен процесс - приёмник собщений с сервера.')
        while self.running:
            # Отдыхаем секунду и снова пробуем захватить сокет.
            # если не сделать тут задержку, то отправка может достаточно долго ждать освобождения сокета.
            time.sleep(1)
            message = None
            with socket_lock:
                try:
                    self.transport.settimeout(0.5)
                    message = get_mes(self.transport)
                except OSError as err:
                    if err.errno:
                        log_client.critical(f'Потеряно соединение с сервером.')
                        self.running = False
                        self.connection_lost.emit()
                # Проблемы с соединением
                except (ConnectionError, ConnectionAbortedError, ConnectionResetError, json.JSONDecodeError, TypeError):
                    log_client.debug(f'Потеряно соединение с сервером.')
                    self.running = False
                    self.connection_lost.emit()
                    # # Если сообщение получено, то вызываем функцию обработчик:
                    # else:
                    #     log_client.debug(f'Принято сообщение с сервера: {message}')
                    #     self.process_server_ans(message)
                    # finally:
                    self.transport.settimeout(5)

            # Если сообщение получено, то вызываем функцию обработчик:
            if message:
                log_client.debug(f'Принято сообщение с сервера: {message}')
                self.process_server_ans(message)
