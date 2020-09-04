import socketserver
import json
import os
from config import settings

ACTION_CODE = {
    '1000': 'cmd',
    '2000': 'post',
    '3000': 'get',
}

REQUEST_CODE = {
    '1001': 'cmd info',
    '1002': 'cmd ack',
    '2001': 'post info',
    '2002': 'ACK（可以开始上传）',
    '2003': '文件已经存在',
    '2004': '续传',
    '2005': '不续传',
    '3001': 'get info',
    '3002': 'get ack',
    '4001': "未授权",
    '4002': "授权成功",
    '4003': "授权失败"
}


class Action(object):
    def __init__(self, conn):
        self.conn = conn
        self.has_login = False
        self.username = None
        self.home = None
        self.current_dir = None

    def initialize(self):
        self.home = os.path.join(settings.USER_HOME, self.username)
        self.current_dir = os.path.join(settings.USER_HOME, self.username)

    def login(self, origin):
        self.conn.sendall('4001'.encode(encoding='utf-8'))

        while True:
            login_str = self.conn.recv(1024).decode(encoding='utf-8')
            print(login_str)
            login_dict = json.loads(login_str)
            if login_dict['username'] == 'alex' and login_dict['password'] == 'alex123':
                self.conn.sendall('4002'.encode(encoding='utf-8'))
                self.has_login = True
                self.username = 'alex'
                self.initialize()
                break
            else:
                self.conn.sendall('4003'.encode(encoding='utf-8'))

    def post(self, origin):
        func, file_size_byte, file_name, file_md5, target_path = origin.split('|')
        file_size = int(file_size_byte)
        target_md5_path = os.path.join(self.home, target_path)
        has_receive = 0

        if os.path.exists(target_md5_path):
            self.conn.sendall('2003'.encode(encoding='utf-8'))
            is_continue = self.conn.recv().decode(encoding='uft-8')
            if is_continue == '2004':
                has_file_size = os.stat(target_md5_path).st_size
                self.conn.sendall(has_file_size.encode(encoding='utf-8'))
                has_receive = has_file_size
                f = open(target_md5_path, 'ab')
            else:
                f = open(target_md5_path, 'wb')
        else:
            self.conn.sendall('2002'.encode(encoding='utf-8'))
            f = open(target_md5_path, 'wb')
        while file_size > has_receive:
            data = self.conn.recv(1024)
            f.write(data)
            has_receive += len(data)
        f.close()

    def get(self):
        pass

    def cmd(self):
        pass


class MultiServerHandler(socketserver.BaseRequestHandler):
    def handle(self):
        conn = self.request
        conn.sendall("欢迎登录".encode(encoding='utf-8'))
        obj = Action(conn)
        while True:
            client_bytes = conn.recv(1024)
            print(client_bytes)
            if not client_bytes:
                break
            client_str = client_bytes.decode(encoding='utf-8')
            print(client_str)
            if obj.has_login:
                o = client_str.split('|', 1)
                if len(o) > 0:
                    func = getattr(obj, o[0])
                    func(client_str)
                else:
                    conn.sendall('输入格式错误'.encode(encoding='uft-8'))
            else:
                obj.login(client_str)
        conn.close()


class MultiServer(object):
    def __init__(self):
        socket = socketserver.ThreadingTCPServer((settings.BIND_HOST, settings.BIND_PORT), MultiServerHandler)
        socket.serve_forever()


