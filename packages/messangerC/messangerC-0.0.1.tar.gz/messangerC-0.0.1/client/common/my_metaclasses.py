# 1. Реализовать метакласс ClientVerifier, выполняющий базовую проверку класса «Клиент»
# (для некоторых проверок уместно использовать модуль dis):
# отсутствие вызовов accept и listen для сокетов;
# использование сокетов для работы по TCP;
# отсутствие создания сокетов на уровне классов, то есть отсутствие конструкций такого вида: class Client: s = socket()
import dis


class ClientVerifier(type):
    '''Метакласс выполняющий базовую проверку класса «Клиент»'''

    def __init__(self, clsname, bases, clsdict):
        # print(bases)
        # print(clsname)
        # print(clsdict)
        methods = []
        for func in clsdict:
            try:
                ret = dis.get_instructions(clsdict[func])
            except TypeError:
                pass
            else:
                for i in ret:
                    if i.opname == 'LOAD_GLOBAL':
                        if i.argval not in methods:
                            methods.append(i.argval)
        # print(methods)
        for command in ('accept', 'listen', 'socket'):
            if command in methods:
                raise TypeError('В классе обнаружено использование запрещённого метода')
        if 'get_mes' in methods or 'send_mes' in methods:
            pass
        else:
            raise TypeError('Отсутствуют вызовы функций, работающих с сокетами.')
        super().__init__(clsname, bases, clsdict)


# 2. Реализовать метакласс ServerVerifier, выполняющий базовую проверку класса «Сервер»:
# отсутствие вызовов connect для сокетов;
# использование сокетов для работы по TCP.
class ServerVerifier(type):
    '''Метакласс выполняющий базовую проверку класса «Сервер»'''

    def __init__(self, clsname, bases, clsdict):
        # print(bases)
        # print(clsname)
        # print(clsdict)
        methods = []
        attrs = []
        for func in clsdict:
            # print(func)
            try:
                ret = dis.get_instructions(clsdict[func])
                # print(ret)
            except TypeError:
                pass
            else:
                for i in ret:
                    # print(i)
                    if i.opname == 'LOAD_GLOBAL':
                        if i.argval not in methods:
                            methods.append(i.argval)
                    elif i.opname == 'LOAD_ATTR':
                        if i.argval not in attrs:
                            attrs.append(i.argval)
        # print(methods)
        if 'connect' in methods:
            raise TypeError('Метод connect недопустим в классе сервер')
        if not ('SOCK_STREAM' in attrs and 'AF_INET' in attrs):
            raise TypeError('Некорректная инициализация сокета.')
        super().__init__(clsname, bases, clsdict)
