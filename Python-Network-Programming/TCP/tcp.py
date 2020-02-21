#一个简单的tcp连接
#例：在终端输入：server “”， 另一终端输入：client 127.0.0.1
import socket, argparse

#因为不知道接受数据量多少所以python没有内置recvall函数
def recvall(sock, length):
    #遇到的一个坑：
    #客户端发16个字符，而我在传参时改为17想看看结果，结果sock.recv()函数停止，没有走后面的if语句
    #没有返回空让我很不相信科学，因为其他tcp相关函数如果字符串已经接收完会自动返回空从而进入if判断。让我陷入沉思，怀疑了很多方面
    #其实是正确的，当输入17时，在下一次循环的时候sock.recv()会一直等待最后一个字符,因为一共16个字符，所以最后一个字符永远等不到
    #而其他的tcp函数比如sock.recv()我设置一次性最多接收16字符，而我发送17个字符，接收一次后下一次接收一个字符，接收完会自动接收一个空
    #我终于又相信了科学。\\*^o^*//  
    data = b''
    while len(data) < length:
        more = sock.recv(length - len(data))
        if not more:
            raise EOFError('was expecting %d bytes but only received' 
                            '%d bytes before the socket closed'
                            % (length, len(data)))
        data += more
    return data

def server(interface, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#socket.SOCK_STREAM：使用流
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)#设置服务器关闭之后立即关闭
    sock.bind((interface, port))
    #listen(n)传入的值, n表示的是服务器拒绝(超过限制数量的)连接之前，操作系统可以挂起的最大连接数量。n也可以看作是"排队的数量"
    sock.listen(3) #套接字进行监听 调用之后该套接字不能进行发送和接受。
    print('listening at :', sock.getsockname())
    while True:
        print('等待接受一个新的连接: ')
        sc, sockname = sock.accept() #返回四元组 sc是本地 sockname是远程
        print('客户端套接字: ', sockname)
        data = recvall(sc, 16) #因为客户端发送16个字符，所以传入16
        print('从客户端接收的数据: ', data.decode('ascii'))
        text = "hello client!!!!"
        sc.sendall(text.encode('ascii'))
        sc.close()
        print('关闭套接字')

def client(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print('系统分配的套接字名称 :', sock.getsockname())
    text = 'hi server!!!!!!!'
    sock.sendall(text.encode('ascii'))
    data = recvall(sock, 16) #服务器返回16个字符
    print('从服务器接收的数据" ', data.decode('ascii'))
    sock.close()#关闭进程前发送文件结束符

if __name__ == '__main__':
    choices = {'server': server, 'client': client}
    parser = argparse.ArgumentParser(description='tcp_test')
    parser.add_argument('role', choices=choices, help='选择server or client')
    parser.add_argument('host')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060)

    args = parser.parse_args()
    function = choices[args.role]
    function(args.host, args.p)
  





