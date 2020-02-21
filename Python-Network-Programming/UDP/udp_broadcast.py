#使用udp进行广播
#例：在一两台机器上输入：server ""运行服务器，并在另一终端中输入：client 广播地址ip
import socket, argparse

BUFSIZE = 65535
def server(interface, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((interface, port))

    print('监听：', sock.getsockname())
    while True:
        data, address = sock.recvfrom(BUFSIZE)
        text = data.decode('ascii')
        print('the client at {} says {!r}'.format(address, text))


def client(network, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) #socket.SO_BROADCAST：客户端能够进行广播
    text = 'Broadcast datagram!'
    sock.sendto(text.encode('ascii'), (network, port))


if __name__ == '__main__':
    choices = {'server': server, 'client': client}
    parser = argparse.ArgumentParser(description='send, receive UDP broadcast')
    parser.add_argument('role', choices=choices)
    parser.add_argument('host')
    parser.add_argument('-p', metavar='port', type=int, default=1060)
    args = parser.parse_args()
    function = choices[args.role]
    function(args.host, args.p)