#数据流封帧的一种模式
#使用tcp发送数据块，并在数据块前加上数据块长度作为其前缀
#因为一个字符可能是由多字节组成的，数据流可能被分割成多个部分。
#比如一个int类型4字节，而我一次最大接收2字节，程序就会先对这两字节解码从而产生错误。
#所以要对数据进行封帧

#可以利用python标准库提供的原生序列化形式pickle。pickle用字符'.'标记结束
#>>> pickle.dumps([5, 6, 7])
#b'\x80\x03]q\x00(K\x05K\x06K\x07e.'
#>>> pickle.loads(b'\x80\x03]q\x00(K\x05K\x06K\x07e.asfsafd') //pickle遇到字符'.'会停止，所以要继续读取.后面的数据
#[5, 6, 7]
#>>> from io import BytesIO
#>>> f = BytesIO(b'\x80\x03]q\x00(K\x05K\x06K\x07e.asfsafd')
#>>> pickle.load(f)
#[5, 6, 7]
#>>> f.tell()
#14
#>>> f.read()
#b'asfsafd'

#需要设计支持其他编成语言的协议或只希望使用通用标准，使用json数据格式
#import json
#json.dumps([51, 'my name is 刘浩泽'])
#'[51, "my name is \\u5218\\u6d69\\u6cfd"]'
#json.dumps([51, 'my name is 刘浩泽'], ensure_ascii=False) //支持Unicode
#'[51, "my name is 刘浩泽"]
#json.loads('{"name": "lancelot", "quest": "Grail"}')
#{'name': 'lancelot', 'quest': 'Grail'}

#在发送数据前对数据进行压缩从而减少传输时间。使用zlib压缩
#zlib能自己进行封帧,如果后面有未压缩的数据也可直接访问

# >>> import zlib
# >>> data = zlib.compress(b'python') + b'.' + zlib.compress(b'zlib') + b'.'
# >>> data
# b'x\x9c+\xa8,\xc9\xc8\xcf\x03\x00\tW\x02\xa3.x\x9c\xab\xca\xc9L\x02\x00\x04d\x01\xb2.'
# >>> len(data)
# 28
# //假设这28B是以每个数据包8B形式发送
# >>> d = zlib.decompressobj()
# >>> d.decompress(data[0:8]), d.unused_data //unused_data槽是空的说明还有数据未处理
# (b'pytho', b'')
# >>> d.decompress(data[8:16]), d.unused_data //我们希望再次运行recv()调用，会返回一个非空unused_data表明已经接收了b'.'这个字节
# (b'n', b'.x')
# >>> d = zlib.decompressobj()
# >>> d.decompress(b'x'), d.unused_data //由于我们正在等待更多压缩数据，因此把'x'传递给一个新解压新对象
# (b'', b'')
# >>> d.decompress(data[16:24]), d.unused_data
# (b'zlib', b'')
# >>> d.decompress(data[24:]), d.unused_data //d.unused_data变得非空表明我们已经读到数据的结尾
# (b'', b'.')



#以下代码只对数据进行封帧，以上的没用到┑(￣▽ ￣)┍
import socket, struct, argparse
# '!'适用于那些声称自己不记得网络字节顺序是大端还是小端的人，I表示传输的数据类型是32位无符号整型
header_struct = struct.Struct('!I')

def recvall(sock, length):
    blocks = []
    while length:
        block = sock.recv(length)
        if not block:
            raise EOFError('socket closed with {} bytes left in this bolck'.format(length))
        blocks.append(block)
        length -= len(block)
        
    return b''.join(blocks)

def get_block(sock):
    #size:对应于的结构的计算大小（以及由此pack()方法生成的字节对象的大小）
    data = recvall(sock, header_struct.size)
    #struct.unpack(fmt, string)用于将字节流转换成python数据类型。该函数返回一个元组，即使他只包含一个项目
    (block_length,) = header_struct.unpack(data)
    data = recvall(sock, block_length)
    return data

def put_block(sock, message):
    block_length = len(message)
    #struct.pack(fmt, v1, v2, ...)，将Python的值根据格式符，转换为字节流，返回字节对象
    #参数fmt是格式字符串因为我们一开始设置了struck(‘！I’),所以这没有设置
    data = header_struct.pack(block_length)
    #data = data + message 可以合一起一起发送
    sock.send(data)
    sock.send(message)

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

if __name__ == '__main__':
    choices = {'server': server, 'client': client}
    parser = argparse.ArgumentParser()
    parser.add_argument('role', choices=choices, help='input server or client')
    parser.add_argument('host')
    parser.add_argument('-p', type=int, default=1060)
    args = parser.parse_args()
    function = choices[args.role]
    function((args.host, args.p))