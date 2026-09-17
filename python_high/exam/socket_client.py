import socket

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

client_socket.connect(('192.168.108.88',8000))

client_socket.send("hello，itheima".encode('utf-8'))

rec_data = client_socket.recv(1024)
print(rec_data.decode('utf-8'))

client_socket.close()


