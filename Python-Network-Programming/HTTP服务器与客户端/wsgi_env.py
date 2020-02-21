from pprint import pformat
from wsgiref.simple_server import make_server

#使用WSGL添加中间层，使服务器具有可移植性
#environ用来接收一个字典， start_response本身也是可以调用的，WSGI应用程序start_response()来声明响头信息
def app(environ, start_response):
    headers = {'Content-Type': 'text/plain; charset=utf-8'}
    start_response('200 OK', list(headers.items()))
    yield 'Here is the WSGI environment:\r\n\r\n'.encode('utf-8')
    yield pformat(environ).encode('utf-8')

if __name__ == '__main__':
    #创建一个侦听主机和端口的新WSGI服务器，接受app的连接
    httpd = make_server('', 8000, app)
    host, port = httpd.socket.getsockname()
    print('server on', host, 'port', port)
    httpd.serve_forever()