#本例中客户端可以询问三个问题，每个问题结尾用‘,‘结束。服务器应答结尾用'.'结束，这两个标点符号相当于提供了封帧功能

import argparse, socket, time, memcache, ssl
ssl.match_hostname = lambda cert, hostname: True

#以下是客户端可以询问的问题，以及客户端的回答
#例如：询问'1:Do one thing at a time,'  回答'and do well.'
aphorisms = {b'1:Do one thing at a time,': b'and do well.',
            b'2:Never forget to say,': b'"thanks".',
            b'3:Keep on going,': b'never give up.',
            b'4:Whatever is worth doing is,': b'worth doing well.',
            b'5:Action speak louder than,': b'words.',
            b'6:Never say,': b'die.',
            b'7:Kings go mad,': b'and the people suffer for it.',
            b'8:Knowledge is,': b'power.'}

#用于读取命令行参数
def parse_command_line(description):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('host', help='')
    parser.add_argument('-p', metavar='port', type=int, default=1060)
    args = parser.parse_args()
    address = (args.host, args.p)
    return address

#创建TCP监听套接字
def creat_srv_socket(address):
    hostname, port = address
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((hostname, port))
    sock.listen(32)
    print('监听：', sock.getsockname())
    return sock

#创建TSL上下文对象
def ssl_context(certfile, cafile = None):
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH, cafile = cafile)
    #上面cafile值为None，然后调用load_cert_chain()安装其他证书，就可以使用两种证书
    context.load_cert_chain(certfile)
    return context

#不断通过监听套接字接受连接
def accept_connections_forever(sock, certfile, cafile = None):
    context = ssl_context(certfile, cafile)
    while True:
        raw_sock, address = sock.accept()
        print('与客户端{}连接'.format(address))
        #wrap_socket()表示让OpenSSL库负责我们tcp连接，返回的该对象提供了普通套接字的所有方法,有两个重要参数选项，分别用于服务端和客户端
        #服务端使用参数server_side=True，通讯双方必须有一方是服务端
        ssl_sock = context.wrap_socket(raw_sock, server_side=True)
        handle_conversation(ssl_sock, address)

#不断处理请求，并捕捉程序可能发生的错误
def handle_conversation(sock, address):
    try:
        while True:
            aphorism = recv_until(sock, b',')
            answer = get_answer(aphorism)
            sock.sendall(answer)
    except EOFError:
        print('客户端套接字{}关闭'.format(address))
    except Exception as e:
        print('客户端套接字{}错误{}'.format(address, e))
    finally:
        sock.close()

#使用memcache缓存
mc = memcache.Client(['127.0.0.1:11211'])
def get_answer(aphorism):
    value = mc.get('say:%s' % aphorism[0:1])
    if value == None:
        time.sleep(1.0) #用来模拟昂贵的操作
        value = aphorisms.get(aphorism)
        if value == None:
            value = 'Error: unknown aphorisms'
        else:
            mc.set('say:%s' % aphorism[0:1], value)
    return value

#接收信息，并用其中一种模式进行封帧
def recv_until(sock, suffix):
    message = sock.recv(1024)
    if not message:
        raise EOFError('sock closed')
    while not message.endswith(suffix):
        data = sock.recv(1024)
        if not data:
            raise IOError('received {!r} then socket closed'.format(message))
        message += data
    return message