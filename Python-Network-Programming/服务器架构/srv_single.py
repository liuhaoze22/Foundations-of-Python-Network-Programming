#单线程服务器
import zen_utils

if __name__ == '__main__':
    address = zen_utils.parse_command_line('simple single-threaded server')
    listener = zen_utils.creat_srv_socket(address)
    zen_utils.accept_connections_forever(listener)