#现代地址解析函数的使用
#连接www（80）端口, 使用socket.getaddrinfo()， 一般不会直接使用dns访问，因为慢
#例： 输入：mit.edu或smtp.baidu.com
import socket, argparse, sys

def connect_to(hostname_or_id):
    #getaddrinfo（host，port，family = 0，type = 0，proto = 0，flags = 0 ）
    #flags: AI_ADDRCONFIG：把无法连接的地址滤掉 AI_CANONNAME：返回主机规范名称 socket.AI_V4MAPPED: ipv4转ipv6 如果连接的服务只支持ipv4那么使用
    #返回(family, type, proto, canonname, sockaddr)
    try:
        infolist = socket.getaddrinfo(hostname_or_id, 'www', 0, socket.SOCK_STREAM, 0,
        socket.AI_ADDRCONFIG | socket.AI_CANONNAME)
    except socket.gaierror as e:
        print('服务器名称错误', e.args[1])
        sys.exit(1)

    info = infolist[0]
    sock = socket.socket(*info[0:3])#把返回中的（family, type, proto）传入

    address = info[4]
    try:
        sock.connect(address)#把返回的(canonname, sockaddr)传入
    except socket.error as e:
        print('网络连接失败：', e.args[1])
    else:
        print('成功连接{},监听端口为{}'.format(address, socket.getservbyname('www')))#socket.getservbyname()获取监听端口80

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='尝试连接www端口号80')
    parser.add_argument('hostname', help='连接什么主机名')
    connect_to(parser.parse_args().hostname)