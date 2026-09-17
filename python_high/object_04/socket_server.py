"""
服务端 被动接收并返回接收数据
"""
import socket
# 创建被动套接字 不用于数据传输
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# 端口号复用
server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,True)
server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEPORT,True)
# 绑定ip地址和端口  -> 客户端通过ip和端口找到对应程序
# 0.0.0.0 表示可以接收所有ip的请求
print("开始绑定端口....")
server_socket.bind(('127.0.0.1',8090))
# 设置监听  被动套接字 -> 监听来自客户端的请求 排队的客户端数量 默认128
print("开始监听....")
server_socket.listen(100)
# 接收客户端请求 被动套接字 return 主动套接字,客户端ip:端口 -> 如果没有客户端连接 则处于阻塞状态
print("准备接收....")
client_socket, client_addr = server_socket.accept()
print("等待程序连接....")
# 接收数据
data = client_socket.recv(1024)
print("接收到客户端数据",data.decode('utf-8'))
# 发送数据
client_socket.send("接收数据成功".encode('utf-8'))
# 关闭套接字资源
client_socket.close()
server_socket.close()














