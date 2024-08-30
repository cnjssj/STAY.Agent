import socket
import json
import threading
from dataclasses import dataclass


# 定义服务器的IP地址和端口号
host, port = "127.0.0.1", 25001


# 处理客户端连接的函数
def handle_client(client_socket):
    send_thread = threading.Thread(target=send_npc_info, args=(client_socket,))
    receive_thread = threading.Thread(target=receive_npc_info, args=(client_socket,))

    send_thread.start()
    receive_thread.start()


# 将NPCInfo实例转为JSON格式并发送给客户端
def send_npc_info(client_socket):
    npc_info = NPCInfo("机器人", 100, 10, 1.5) # 示例数据
    while True:
        user_input = input("输入P发送信息")
        if user_input.lower() == 'p':
            json_data = json.dumps(npc_info.__dict__) # 转换为JSON格式
            json_data += '\n' # 添加换行符作为分隔符
            client_socket.sendall(json_data.encode()) # 发送JSON数据


# 从客户端接收JSON数据并解码为NPCInfo实例
def receive_npc_info(client_socket):
    while True:
        received_data = client_socket.recv(1024).decode() # 接收数据并解码为字符串
        if not received_data:
            break
        # 解码JSON数据为NPCInfo实例
        npc_data = json.loads(received_data)
        npc_info = NPCInfo(**npc_data)
        print("收到Unity信息:", npc_info)

# 创建TCP socket并绑定IP地址和端口号
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(5)

print(f"正在监听 {host}:{port}")

while True:
    # 等待客户端连接
    client_socket, _ = server_socket.accept()
    print(f"成功连接到客户端 {_}")

    # 启动一个线程来处理客户端连接
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()