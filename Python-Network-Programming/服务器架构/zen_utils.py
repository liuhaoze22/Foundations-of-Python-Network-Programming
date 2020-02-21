#本例中客户端可以询问三个问题，每个问题结尾用‘?‘结束。服务器应答结尾用'.'结束，这两个标点符号相当于提供了封帧功能

import argparse, socket, time

#以下是客户端可以询问的问题，以及客户端的回答
aphorisms = {b'Beautiful is better than?': b'Ugly.',
            b'Explicit is better than?': b'Implicit.',
            b'Simple is better than?': b'Complex.'}

def get_answer(aphorism):
    time.sleep(1.0) #用来模拟昂贵的操作
    return aphorisms.get(aphorism, b'Error: unknown aphorisms')

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
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind(address)
    listener.listen(32)
    print('监听：', listener.getsockname())
    return listener

#不断通过监听套接字接受连接
def accept_connections_forever(listener):
    while True:
        sock, address = listener.accept()
        print('接受{}的连接'.format(address))
        handle_conversation(sock, address)

#不断处理请求，并捕捉程序可能发生的错误
def handle_conversation(sock, address):
    try:
        while True:
            handle_request(sock)
    except EOFError:
        print('客户端套接字{}关闭'.format(address))
    except Exception as e:
        print('客户端套接字{}错误{}'.format(address, e))
    finally:
        sock.close()

#读取客户端的问题，然后作出回答
def handle_request(sock):
    aphorism = recv_until(sock, b'?')
    answer = get_answer(aphorism)
    sock.sendall(answer)

#接收信息，并用其中一种模式进行封帧
def recv_until(sock, suffix):
    message = sock.recv(4096)
    if not message:
        raise EOFError('sock closed')
    while not message.endswith(suffix):
        data = sock.recv(4096)
        if not data:
            raise IOError('received {!r} then socket closed'.format(message))
        message += data
    return message