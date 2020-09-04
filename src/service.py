import socketserver
from config import settings


class MultiServerHandler(socketserver.BaseRequestHandler):
    def handle(self):
        pass


class MultiServer(object):
    def __init__(self):
        socket = socketserver.ThreadingTCPServer((settings.BIND_HOST, settings.BIND_PORT), MultiServerHandler)
        socket.serve_forever()


