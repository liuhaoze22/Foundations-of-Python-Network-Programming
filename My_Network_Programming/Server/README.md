zen_utils.py是作为一个服务器支持性模块，使用TLS加密传输和memcache缓存。由srv_threaded.py和srv_async.py导入。

client.py是为测试服务器所写的客户端，使用ca.crt证书

srv_threaded.py是多线程服务器，服务器使用localhost.pem证书

srv_async.py是异步服务器。同样使用localhost.pem证书

使用说明：
    因为需要要用memcache缓存，需要安装memcache，使用'pip install python3-memcached'命令安装

    1.使用多线程服务器：
    运行srv_threaded.py，运行时在命令行输入相应主机ip地址，默认端口1060
    如：
    srv_threaded.py 192.168.0.115
![Image text](https://raw.githubusercontent.com/liuhaoze22/Foundations-of-Python-Network-Programming/master/My_Network_Programming/Server/img-folder/srv_threaded.PNG)
    运行clinet.py，运行时输入服务器的ip地址。可ctrl+Z挂起服务器，在不同的终端输入多个客户端，在使用fg启动服务器，便可以看到多个客户端同时访问
    如!
    client.py 192.168.0.115
![Image text](https://raw.githubusercontent.com/liuhaoze22/Foundations-of-Python-Network-Programming/master/My_Network_Programming/Server/img-folder/client.PNG)

    2.使用异步服务器：
    运行srv_async.py, 运行时在命令行输入相应主机ip地址，默认端口1060
    如：
![Image text](https://raw.githubusercontent.com/liuhaoze22/Foundations-of-Python-Network-Programming/master/My_Network_Programming/Server/img-folder/srv_async.PNG)

    运行client.py,运行时输入服务器的ip地址。可ctrl+Z挂起服务器，在不同的终端输入多个客户端，在使用fg启动服务器，便可以看到多个客户端同时访问
        如：
![Image text](https://raw.githubusercontent.com/liuhaoze22/Foundations-of-Python-Network-Programming/master/My_Network_Programming/Server/img-folder/client1.PNG)

