#一个简单的异步事件循环
#从服务器向客户端发送响应到接收客户端下一个请求有一段时间的间隔，此时cpu处于等待状态
#使用异步模式来编写服务器，使cpu一直处于繁忙状态，
#使用这种模式代码就不需要等待数据发送至某个特定的客户端或由这个客户端接收
#相反，代码可以从整个处于等待的客户端套接字列表中读取数据

import select, zen_utils

def all_events_forever(poll_object):
    while True:
        #轮询已注册文件描述符的集合，其中包含要报告事件或错误的描述符的2元组。
        #fd是文件描述符，而event是一个位掩码，位掩码表示是select.POLLOUT，select.POLLIN等
        #使用yield组合成一个生成器
        for fd, event in poll_object.poll():
            yield fd, event

def server(listener, certfile):
    #套接字列表，fileno()返回套接字的文件描述符（一个小整数）
    context = zen_utils.ssl_context(certfile, cafile = None)
    listener = context.wrap_socket(listener, server_side=True)
    sockets = {listener.fileno(): listener}
    addresses = {}
    #两个缓冲队列用于接收和发送
    bytes_received = {}
    bytes_to_send = {}
    #返回一个轮询对象，该对象支持注册和注销文件描述符，然后对它们进行轮询以获取I / O事件
    poll_object = select.poll()
    #向轮询对象注册文件描述符，然后用poll()函数检查文件描述符是否具有任何未决的I / O事件，下面是注册监听套接字文件描述符
    poll_object.register(listener, select.POLLIN)

    for fd, event in all_events_forever(poll_object):
        sock = sockets[fd]
        #判断是不是客户端是不是关了或发生了错误或是无效请求
        if event & (select.POLLHUP | select.POLLERR | select.POLLNVAL):
            address = addresses.pop(sock)
            rb = bytes_received.pop(sock, b'')
            sb = bytes_to_send.pop(sock, b'')
            if rb:
                print('客户端{}发送{}但服务器已关闭'.format(address, rb))
            elif sb:
                print('服务器发送{}但客户端{}已关闭'.format(address, sb))
            else:
                print('客户端{}套接字正常关闭'.format(address))
            poll_object.unregister(fd)
            del sockets[fd]
        #如果取出的套接字是监听套接字
        elif sock is listener:
            sock, address = sock.accept()
            print('接受客户端{}连接'.format(address))
            # 在默认认的情况下,TCP套节字处于阻塞模式中。
            # 换句话说,如果没有完成操作,就不把控制权交给程序。
            # 很多情况下,你并不想让程序等待服务器响应或者有异常终止操作，所以设置非阻塞模式。
            sock.setblocking(False)
            #把建立的服务器套接字放入套接字列表中
            sockets[sock.fileno()] = sock
            #把接收到的客户端套接字地址放入地址列表中
            addresses[sock] = address
            #注册该服务器套接字，以供poll()调用
            poll_object.register(sock, select.POLLIN)
        #判断该套接字位掩码event是不是POLLIN
        elif event & select.POLLIN:
            more_data = sock.recv(1024)
            if not more_data:
                sock.close()
                continue
            data = bytes_received.pop(sock, b'') + more_data
            if data.endswith(b','):
                #如果信息传输完成，把数据保存在发送缓冲队列中，并把该套接字事件设为select.POLLOUT输出
                bytes_to_send[sock] = zen_utils.get_answer(data)
                poll_object.modify(sock, select.POLLOUT)
            else:
                #如果只接收了部分数据，把该数据保存到接收缓冲队列中
                bytes_received[sock] = data
        #判断该套接字位掩码event是不是POLLOUT
        elif event & select.POLLOUT:
            #把数据从发送缓冲队列中弹出并发送，并把事件设置为select.POLLIN输入
            data = bytes_to_send.pop(sock)
            n = sock.send(data)
            if n < len(data):
                bytes_to_send[sock] = data[n:]
            else:
                poll_object.modify(sock, select.POLLIN)

if __name__ == '__main__':
    address = zen_utils.parse_command_line('')
    listener = zen_utils.creat_srv_socket(address)
    certfile = '/home/liu/code/Python_Network_Programming/My_Network_Programming/localhost.pem'
    server(listener, certfile)