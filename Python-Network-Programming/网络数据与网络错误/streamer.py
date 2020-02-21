#极简单的传输模式，只关注接收而不关注响应
#发送方循环发送数据直到传送完为止，接收端循环接收直至接收到空字符串

import socket, argparse

def server(address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(3)
    print('监听：', sock.getsockname())
    sc, sockname = sock.accept()
    print('接收到客户端套接字：', sockname)
    sc.shutdown(socket.SHUT_WR)
    message = b''
    while True:
        more = sc.recv(10)
        if not more:
            print('接收完成')
            break
        print('接收{}bytes'.format(len(more)))
        message += more

    print('从客户端接收：')
    print(message.decode('ascii'))
    sc.close()
    sock.close()

def client(address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(address)
    sock.shutdown(socket.SHUT_RD)
    text1 = 'I love you\n' #11个字符
    text2 = 'I love you very much\n' #21
    text3 = 'I love you very very much\n' #26
    sock.sendall(text1.encode('ascii'))
    sock.sendall(text2.encode('ascii'))
    sock.sendall(text3.encode('ascii'))

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