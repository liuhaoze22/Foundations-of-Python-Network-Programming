#会造成混杂客户端和垃圾回复 客户端sendto()可以检查响应数据包的返回地址，看是否曾经请求过
#将服务器ctrl+z挂起，客户端访问服务器时会等待服务器响应，此时打开另一个终端并打开python3命令行输入以下代码，
#客户端会接受信息并关闭，而此信息并不是服务器发出。
#python3
#import socket
#sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#sock.sendto('fake'.encode('ascii'), ('127.0.0.1', 43716))

#可以使用在请求中使用唯一标识符或请求id的协议，在响应中重复特定请求的唯一标识符或请求id。如果响应包含了id，那么说明该响应来自服务器
#或者使用connect()连接
#例：在终端输入：server。 另一终端输入：client
import argparse, socket
from datetime import datetime

MAX_BYTES = 65535

def server(port) :
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)#socket.SOCK_DGRAM：使用数据报
    sock.bind(('127.0.0.1', port)) #给定服务器ip地址和端口号
    print('listening at {}'.format(sock.getsockname()))

    while True:
        data, address = sock.recvfrom(MAX_BYTES) #recvfrom返回两个参数 客户端发送的字节串和客户端（ip地址，端号）
        text = data.decode('ascii') #解码：将字节串转为字符串
        print('the client at {} says {!r}'.format(address, text))
        text = 'your data was {} bytes long'.format(len(data))
        data = text.encode('ascii') #编码：采用ascii编码，将字符串转为字节串
        sock.sendto(data, address) #sendto发送数据到客户端

def client(port) :
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    text = input('please input: ')
    data = text.encode('ascii') 
    sock.sendto(data, ('127.0.0.1', port))
    print('the OS assigned me the address {}'.format(sock.getsockname()))
    data, address = sock.recvfrom(MAX_BYTES) 
    text = data.decode('ascii')
    print('the server{} replied {!r}'.format(address, text))      



if __name__ == '__main__' :
    choices = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description='send and receive UDP locally')
    parser.add_argument('role', choices=choices, help='which role to play')
    parser.add_argument('-p', metavar='POST', type=int, default=1060)
    args = parser.parse_args()
    funtion = choices[args.role]
    funtion(args.p)




