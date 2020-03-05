import argparse, random, socket, zen_utils, ssl
ssl.match_hostname = lambda cert, hostname: True

def client(address, cafile):
    hostname, port = address
    #ssl.Purpose.SERVER_AUTH参数表示该上下文对象为客户端所用
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile = cafile)
    raw_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    raw_sock.connect((hostname, port))
    print('连接服务器:{}端口:{}'.format(hostname, port))
    ssl_sock = context.wrap_socket(raw_sock, server_hostname=hostname)

    #提出字典的键去访问服务器
    aphorisms = list(zen_utils.aphorisms)
    for aphorism in random.sample(aphorisms, 3):
        ssl_sock.sendall(aphorism)
        print(aphorism, zen_utils.recv_until(ssl_sock, b'.'))
    ssl_sock.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Example client')
    parser.add_argument('host', help='IP or hostname')
    parser.add_argument('-p', metavar='port', type=int, default=1060, help='TCP port (default 1060)')
    args = parser.parse_args()
    address = (args.host, args.p)
    cafile = 'Foundations-of-Python-Network-Programming/My_Network_Programming/Server/ca.crt'
    client(address, cafile)