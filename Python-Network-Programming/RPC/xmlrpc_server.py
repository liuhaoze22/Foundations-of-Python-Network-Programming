#XML-RPC server服务器

import operator, math
from xmlrpc.server import SimpleXMLRPCServer
from functools import reduce

def main():
    #标准库提供的SimpleXMLRPCServer()相当简单，不支持其他Web页面的访问
    server = SimpleXMLRPCServer(('127.0.0.1', 7001))
    #register_introspection_functions()会启动一个用于自省的服务
    server.register_introspection_functions()
    #register_introspection_functions()允许将多个独立的函数调用打包在同一个网络往返中
    server.register_multicall_functions()
    server.register_function(addtogether)
    server.register_function(quadratic)
    server.register_function(remote_repr)
    print("Server ready")
    server.serve_forever()

def addtogether(*things):
    """Add together everything in the list `things`."""
    return reduce(operator.add, things)

def quadratic(a, b, c):
    """Determine `x` values satisfying: `a` * x*x + `b` * x + c == 0"""
    b24ac = math.sqrt(b*b - 4.0*a*c)
    return list(set([ (-b-b24ac) / 2.0*a,
                      (-b+b24ac) / 2.0*a ]))

def remote_repr(arg):
    """Return the `repr()` rendering of the supplied `arg`."""
    return arg

if __name__ == '__main__':
    main()
