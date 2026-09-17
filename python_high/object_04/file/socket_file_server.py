import socket

# 创建被动套接字 不用于数据传输
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,True)

server_socket.bind(('127.0.0.1',9999))

server_socket.listen(5)
print("开始等待连接...")

print("准备传输...")

count = 0
while True:
    count += 1
    client_socket, client_addr = server_socket.accept()
    with open(f"server{count}.gif",'wb') as f:
        while True:
            client_data = client_socket.recv(1024)
            if not client_data:
                break
            f.write(client_data)
        print("客户端传输完毕...")
    client_socket.close()



