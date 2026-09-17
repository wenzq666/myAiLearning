"""
套接字
进程间的通信工具

数据传输的载体

服务端 2个套接字
客户端 1个套接字
"""
import socket

# AF_INET --> ipv4               / AF_INET6 --> ipv6
# SOCK_STREAM --> TCP协议        / SOCK_DGRAM --> UDP协议
tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print(tcp_server_socket)

print('==='*20)
str_date = "锟斤拷"

bytes_data = str_date.encode('gb2312')
print(type(bytes_data),bytes_data)

print('==='*20)
bytes2str_data = bytes_data.decode('utf-8',errors='replace')
print(type(bytes2str_data),bytes2str_data)


















