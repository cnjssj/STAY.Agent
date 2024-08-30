import socket
import threading
from Server.JsonHandler import JSONHandler


# 定义服务器的IP地址和端口号
class ServerConfig:
    def __init__(self, host="127.0.0.1", port=25001):
        self.host = host
        self.port = port

# 客户端请求的数据结构
class ClientRequest:
    def __init__(self, request: str):
        self.request = request

# 服务器响应的数据结构
class ServerResponse:
    def __init__(self, expression: str):
        self.expression = expression

# 通用的客户端处理类
class ClientHandler:
    def __init__(self, client_socket, data_handler: JSONHandler):
        self.client_socket = client_socket
        self.data_handler = data_handler
        self.send_callback = None
        self.receive_callback = None
        self.send_thread = None
        self.receive_thread = None

    def start(self):
        if self.send_callback and self.receive_callback:
            self.send_thread = threading.Thread(target=self.send_data)
            self.receive_thread = threading.Thread(target=self.receive_data)
            self.send_thread.start()
            self.receive_thread.start()
        else:
            raise ValueError("send_callback 和 receive_callback 必须在调用 start() 前设置")

    def set_send_callback(self, send_callback):
        self.send_callback = send_callback

    def set_receive_callback(self, receive_callback):
        self.receive_callback = receive_callback

    def send_data(self):
        self.send_callback(self.client_socket, self.data_handler)

    def receive_data(self):
        self.receive_callback(self.client_socket, self.data_handler)

# 通用的TCP服务器类
class TCPServer:
    def __init__(self, config: ServerConfig, data_handler: JSONHandler):
        self.config = config
        self.handler_cls = ClientHandler
        self.data_handler = data_handler
        self.send_callback = None
        self.receive_callback = None

    def set_send_callback(self, send_callback):
        self.send_callback = send_callback

    def set_receive_callback(self, receive_callback):
        self.receive_callback = receive_callback

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.config.host, self.config.port))
        server_socket.listen(5)

        print(f"正在监听 {self.config.host}:{self.config.port}")

        while True:
            client_socket, addr = server_socket.accept()
            print(f"成功连接到客户端 {addr}")

            client_handler = self.handler_cls(client_socket, self.data_handler)

            if self.send_callback:
                client_handler.set_send_callback(self.send_callback)

            if self.receive_callback:
                client_handler.set_receive_callback(self.receive_callback)

            client_thread = threading.Thread(target=client_handler.start)
            client_thread.start()

