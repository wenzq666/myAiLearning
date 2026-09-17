import socket

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# client_socket.connect(('192.168.138.26',8888))
client_socket.connect(('127.0.0.1',9999))
print("准备传输....")
with open('13400932962986622.gif','rb') as f:
    while True:
        data = f.read(1024)
        if not data:
            break
        client_socket.send(data)
    print("传输完成....")
    client_socket.close()










