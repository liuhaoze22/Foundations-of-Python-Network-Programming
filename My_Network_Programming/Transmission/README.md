1.UDP.py是使用udp协议进行传输，此例模拟了丢包，并使用使用指针退避技术，通过这一技术重发数据包的频率越来越底

例：
输入：UDP.py server 192.168.0.115 启动服务器监听
![Image text](https://raw.githubusercontent.com/liuhaoze22/Foundations-of-Python-Network-Programming/master/My_Network_Programming/Transmission/img-folder/udp_server.PNG)

输入：UDP.py client 192.168.0.115 启动客户端发送数据
![Image text](https://raw.githubusercontent.com/liuhaoze22/Foundations-of-Python-Network-Programming/master/My_Network_Programming/Transmission/img-folder/udp_client.PNG)
![Image text](https://raw.githubusercontent.com/liuhaoze22/Foundations-of-Python-Network-Programming/master/My_Network_Programming/Transmission/img-folder/udp_client1.PNG)


2.TCP.py是使用tcp协议进行传输,使用在消息前面加上其长度的封帧模式
![Image text](https://raw.githubusercontent.com/liuhaoze22/Foundations-of-Python-Network-Programming/master/My_Network_Programming/Transmission/img-folder/TCP_server.PNG)


![Image text](https://raw.githubusercontent.com/liuhaoze22/Foundations-of-Python-Network-Programming/master/My_Network_Programming/Transmission/img-folder/TCP_client.PNG)

