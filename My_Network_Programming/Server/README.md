zen_utils.py是作为一个服务器支持性模块，使用TLS加密传输和memcache缓存。由srv_threaded.py和srv_async.py导入。

client.py是为测试服务器所写的客户端，使用ca.crt证书

srv_threaded.py是多线程服务器，服务器使用localhost.pem证书

srv_async.py是异步服务器。同样使用localhost.pem证书

使用说明：
    因为需要要用memcache缓存，需要安装memcache，使用'pip install python3-memcached'命令安装

    1.使用多线程服务器：
    运行srv_threaded.py，运行时在命令行输入相应主机ip地址
    如：
