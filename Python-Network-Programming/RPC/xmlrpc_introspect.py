#请求获取某XML-RPC server服务器支持的函数

import xmlrpc.client

def main():
    proxy = xmlrpc.client.ServerProxy('http://127.0.0.1:7001')

    print('Here are the functions supported by this server:')
    #调用listMethods()如果服务器支持自省功能该函数就会返回一个列表，列表包含其他方法的名字
    for method_name in proxy.system.listMethods():
        #通过自省机制，客户端可以调用一系列以system字符串开头的特殊方法
        if method_name.startswith('system.'):
            continue
            
        signatures = proxy.system.methodSignature(method_name)
        if isinstance(signatures, list) and signatures:
            for signature in signatures:
                print('%s(%s)' % (method_name, signature))
        else:
            print('%s(...)' % (method_name,))

        method_help = proxy.system.methodHelp(method_name)
        if method_help:
            print('  ', method_help)

if __name__ == '__main__':
    main()
