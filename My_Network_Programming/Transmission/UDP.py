#使用connect()连接能避免混杂客户端和垃圾回复，操作系统发现传入的数据包的返回地址与以连接的地址不同会丢弃该数据包。
#该程序模拟了udp传输可能会丢包的情况
#例：在终端输入：server 本机ip. 另一终端输入：client 要连接的服务器ip
import socket, random, argparse

MAX_BYTES = 65535
def server(interface, port) :
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((interface, port))
    print('监听：', sock.getsockname())
    while True :
        data, address = sock.recvfrom(MAX_BYTES) #返回字节串data和客户端address
        if random.random() > 0.3:#使用随机数模拟丢包
            print('{}的数据丢包'.format(address))
            continue
        text = data.decode('utf-16')
        print('从客户端:{} 接受到：{}'.format(address, text))
        text = '以收到 你的字符长度为: {}'.format(len(text))
        data = text.encode('utf-16')
        sock.sendto(data, address)

def client(hosthome, port) :
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect((hosthome, port)) #使用connect()
    print('客户端地址： {}'.format(sock.getsockname()))
    delay = 0.1 #使用指针退避技术，通过这一技术重发数据包的频率越来越底
    print('输入您要输入的数据: ')
    text = input()
    data = text.encode('utf-16')

    while True :
        sock.send(data)
        print('等待 {} 秒后重新发送'.format(delay))
        sock.settimeout(delay)
        try:
            data = sock.recv(MAX_BYTES)
        except socket.timeout:
            delay *= 2
            if delay > 2:
                raise RuntimeError('服务器可能掉线了')
        else:
            break
    text = data.decode('utf-16')
    print('从服务端收到：{}'.format(text))


if __name__ == '__main__' :
    choices = {'server': server, 'client': client}
    parser = argparse.ArgumentParser('模拟丢包')
    parser.add_argument('role', choices=choices, help='选择server or client')
    parser.add_argument('host')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060)

    args = parser.parse_args()
    function = choices[args.role]
    function(args.host, args.p)



