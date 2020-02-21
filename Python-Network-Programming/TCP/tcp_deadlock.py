#使用sock.shutdown(socket.SHUT_WR)
#可能会发生死锁的tcp 
#因为此代码服务端先接收所有数据，处理后在一起发送到客户端
#1.服务端revc数据转为大写后sendall. 2.由于客户端没有revc数据所以导致客户端接收缓冲区满.
#3.从而使服务端sendall阻塞，由于阻塞导致服务端不能继续运行，从而使revc没有办法接受数据
#4。导致服务端接收缓冲区满，从而导致客户的sandall阻塞。所以死锁。
#例：在终端输入：server “”， 另一终端输入：client “” 16000000
import socket, argparse, sys

def server(interface, port, bytecount):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((interface, port))
    sock.listen(1)
    print('监听:', sock.getsockname())
    while True:
        sc, sockname = sock.accept()
        print('客户端套接字名称:', sockname)
        while True:
            data = sc.recv(1024)
            if not data:
                break
            text = data.decode('ascii')
            output = text.upper().encode('ascii')
            sc.sendall(output)

            sys.stdout.flush()
        
        sc.close()
        print('套接字关闭')


def client(host, port, bytecount):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.connect((host, port))
    bytecount = (bytecount + 15) // 16 * 16
    message = 'hello ya!!!!!!!!'
    sent = 0
    while sent <= bytecount:
        sock.sendall(message.encode('ascii'))
        sent += len(message)
        print('%d 字节以发送' %(sent,))
        sys.stdout.flush()
    #参数shut_rdwr双向关闭与close不同，closer仅关闭调用的他的那个进程，而参数shut_rdwr是所有进程都不能访问
    #关闭双向连接中的任意一方 shut_wr表示不再写入数据 shut_rd表示关闭接受方向的套接字流 
    #此函数关闭一个向连接之前会把缓冲区内容发送完，在发送文件结束符，之后在关闭。
    sock.shutdown(socket.SHUT_WR) 

    received = 0
    while True:
        data = sock.recv(1024)
        if not received:
            print('接收数据:\n', data.decode('ascii'))
        if not data:
            break
        received += len(data)
        print('%d 字节已被接收\n' %(received,))

    sock.close()

if __name__ == '__main__':
    choices = {'server': server, 'client': client}
    parser = argparse.ArgumentParser(description=' ')
    parser.add_argument('role', choices=choices, help='choices server or client')
    parser.add_argument('host', help='input ip address')
    parser.add_argument('bytecount', type=int, nargs='?', default=16)
    parser.add_argument('-p', metavar='PROT', type=int, default=1060)
    args = parser.parse_args()
    function = choices[args.role]
    function(args.host, args.p, args.bytecount)

    