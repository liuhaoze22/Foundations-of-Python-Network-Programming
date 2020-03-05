import socket, struct, argparse
# '!'适用于那些声称自己不记得网络字节顺序是大端还是小端的人，I表示传输的数据类型是32位无符号整型
header_struct = struct.Struct('!I')

#server()是服务器代码，建立监听套接字后用一个循环调用get_block()。
#get_block()先接收数据块的大小，然后根据数据长度使用recvall()。
#recvall()函数用于接收客户端传输的数据。

#client()是客户端代码，调用put_block()来发送数据。
#put_block()先计算发送数据长度存在struct.pack里并发送，在发送数据。

def server(address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(3)
    print('监听：', sock.getsockname())
    sc, sockname = sock.accept()
    print('接收到客户端套接字：', sockname)
    sc.shutdown(socket.SHUT_WR)
    while True:
        block = get_block(sc)
        if not block:
            break
        print('接收到：', block)
    
    sc.close()
    sock.close()

def get_block(sock):
    #size:对应于的结构的计算大小（以及由此pack()方法生成的字节对象的大小）
    data = recvall(sock, header_struct.size)
    #struct.unpack(fmt, string)用于将字节流转换成python数据类型。该函数返回一个元组，即使他只包含一个项目
    (block_length,) = header_struct.unpack(data)
    data = recvall(sock, block_length)
    return data

def recvall(sock, length):
    blocks = []
    while length:
        block = sock.recv(length)
        if not block:
            raise EOFError('socket closed with {} bytes left in this bolck'.format(length))
        blocks.append(block)
        length -= len(block)
        
    return b''.join(blocks)


def client(address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(address)
    sock.shutdown(socket.SHUT_RD)
    put_block(sock, b'hello')
    put_block(sock, b'hello hello')
    put_block(sock, b'hello hello hello')
    put_block(sock, b'hello hello hello hello hello hello')
    #因为数据块长度做为前缀，接收这个每个数据块时这个前缀并不自动清0，所以最后发送一个长度为0的消息表示所有数据以发送完成
    put_block(sock, b'')
    sock.close()

def put_block(sock, message):
    block_length = len(message)
    #struct.pack(fmt, v1, v2, ...)，将Python的值根据格式符，转换为字节流，返回字节对象
    #参数fmt是格式字符串因为我们一开始设置了struck(‘！I’),所以这没有设置
    data = header_struct.pack(block_length)
    #data = data + message 可以合一起一起发送
    sock.send(data)
    sock.send(message)

if __name__ == '__main__':
    choices = {'server': server, 'client': client}
    parser = argparse.ArgumentParser()
    parser.add_argument('role', choices=choices, help='input server or client')
    parser.add_argument('host')
    parser.add_argument('-p', type=int, default=1060)
    args = parser.parse_args()
    function = choices[args.role]
    function((args.host, args.p))