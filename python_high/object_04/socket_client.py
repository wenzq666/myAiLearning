import socket

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)


#client_socket.connect(('192.168.138.64',8888))
client_socket.connect(('127.0.0.1',9998))

client_socket.send("锟斤拷烫็็็็็็็.?".encode('utf-8'))

rec_data = client_socket.recv(1024)
print(rec_data.decode('utf-8'))

client_socket.close()


