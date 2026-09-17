import socket
import threading
import time

# 被动套接字
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,True)
server_socket.bind(('127.0.0.1',9998))

print("等待客户端连接.....")
server_socket.listen(5)

def handle_client(client_socket, client_addr):
    print(f"{client_addr}")
    with client_socket:
        while True:
            try:
                data = client_socket.recv(1024)
                if len(data) == 0:
                    break
                print(f"客户端数据:{data.decode('utf-8')}")
            except:
                pass




while True:
    client_socket, client_addr = server_socket.accept()
    t = threading.Thread(target=handle_client,args=(client_socket, client_addr))
    t.start()