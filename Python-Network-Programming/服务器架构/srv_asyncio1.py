#回调风格的异步服务器,使用内部框架实现
import asyncio, zen_utils

#继承Protocol
class ZenServer(asyncio.Protocol):
    #建立连接时调用
    def connection_made(self, transport):
        self.transport = transport
        #返回有关其使用的传输或基础资源的信息,'peername'：套接字所连接的远程地址，'socket'：socket.socket实例'，sockname'：套接字自身的地址
        self.address = transport.get_extra_info('peername')
        self.data = b''
        print('接收客户端{}连接'.format(self.address))
    
    #收到一些数据时调用
    def data_received(self, data):
        self.data += data
        if self.data.endswith(b'?'):
            answer = zen_utils.get_answer(self.data)
            #向传输中写入一些数据字节。此方法不会阻塞；它缓冲数据并安排将其异步发送出去。
            self.transport.write(answer)
            self.data = b''

    def connection_lost(self, exc):
        if exc:
            print('客户端{}错误{}'.format(self.address, exc))
        elif self.data:
            print('客户端{}发送{}但是服务器关闭')
        else:
            print('客户端{}关闭'.format(self.address))

if __name__ == '__main__':
    address = zen_utils.parse_command_line('')
    #获取当前事件循环。
    loop = asyncio.get_event_loop()
    #创建一个SOCK_STREAM侦听主机地址端口的TCP服务器。返回一个Server对象。
    coro = loop.create_server(ZenServer, *address)
    #运行直到Future（的一个实例Future）完成。
    server = loop.run_until_complete(coro)
    print('监听：', address)
    try:
        #运行事件循环直到stop()被调用
        loop.run_forever()
    finally:
        server.close()
        loop.close()