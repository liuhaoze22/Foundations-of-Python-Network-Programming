#多线程服务器
import zen_utils
from threading import Thread

def start_threads(listener, workers = 4):
    certfile = '/home/liu/code/Python_Network_Programming/My_Network_Programming/localhost.pem'
    t = (listener, certfile)
    for i in range(workers):
        #target是该run()方法要调用的可调用对象。默认为None，表示什么都不会调用。args是目标调用的参数元组
        Thread(target=zen_utils.accept_connections_forever, args=t).start()

if __name__ == '__main__':
    address = zen_utils.parse_command_line('多线程服务器')
    listener = zen_utils.creat_srv_socket(address)
    
    start_threads(listener)