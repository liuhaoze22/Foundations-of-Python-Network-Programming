#通过TSL提供套接字的安全通信
#TLS客户端需要证书，证书包含了公钥。如果远程服务器配置正确并没有破解那么他将是互联网上唯一拥有该私钥的服务器
#为了验证证书的合法性，CA(证书机构)会给证书一个数学标记，叫做签名。TLS库使用相应CA证书的公钥验证证书的签名后，才会认为证书的合法的
#本例采用简单的localhost证书和对该证书进行签字的CA
#python标准库中没用提供私钥生成或证书签名的操作。可以使用openssl命令行工具
#例:服务端: 192.168.0.115 1060 -s Python-Network-Programming/TLS/SSL/localhost.pem
#  客户端:  192.168.0.115 1060 -a Python-Network-Programming/TLS/SSL/ca.crt

import argparse, socket, ssl
#证书不匹配问题,对于python自带的urllib库解决办法↓ 
ssl.match_hostname = lambda cert, hostname: True

def server(hostname, port, certfile, cafile = None):
    #cafile的默认值为None，此时create_default_context会自动调用新建上下文对象的load_default_certs方法
    #该方法会尝试加载所有默认CA（证书机构）证书，如果将cafile设置为一个字符串，字符串指定一个文件夹名
    #那么TLS连接远程端点时，只会信任该文件中包含的CA证书
    #Purpose.CLIENT_AUTH参数表示该上下文对象用于一个需要接收客户端连接的服务器
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH, cafile = cafile)
    #上面cafile值为None，然后调用load_cert_chain()安装其他证书，就可以使用两种证书
    context.load_cert_chain(certfile)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((hostname, port))
    sock.listen(3)
    print('监听：', sock.getsockname())
    raw_sock, address = sock.accept()
    print('与客户端{}连接'.format(address))
    #wrap_socket()表示让OpenSSL库负责我们tcp连接，返回的该对象提供了普通套接字的所有方法,有两个重要参数选项，分别用于服务端和客户端
    #服务端使用参数server_side=True，通讯双方必须有一方是服务端
    ssl_sock = context.wrap_socket(raw_sock, server_side=True)
    ssl_sock.sendall('hello ya'.encode('ascii'))
    ssl_sock.close()

def client(hostname, port, cafile = None):
    #ssl.Purpose.SERVER_AUTH参数表示该上下文对象为客户端所用
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile = cafile)
    raw_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    raw_sock.connect((hostname, port))
    print('连接服务器为{}端口{}'.format(hostname, port))
    #客户端调用信息需要提供连接的主机名，这样可以将他与服务器提供的证书的subject字段进行比对，这一检查十分重要，
    #server_hostname关键字提供给wrap_socket()检查会自动开始
    ssl_sock = context.wrap_socket(raw_sock, server_hostname=hostname)
    while True:
        data = ssl_sock.recv(1024)
        if not data:
            break
        print(data)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('hostname', help='')
    parser.add_argument('port', type=int, help='')
    parser.add_argument('-a', metavar='cafile', default=None, help='')
    parser.add_argument('-s', metavar='certfile', default=None, help='')
    args = parser.parse_args()

    if args.s:
        server(args.hostname, args.port, args.s, args.a)
    else:
        client(args.hostname, args.port, args.a)