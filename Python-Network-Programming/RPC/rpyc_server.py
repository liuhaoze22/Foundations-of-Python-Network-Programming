#使用需要直接传递Python对象，协调使用网络上不同的位置的Python对象的话，RPyC确实是最好的选择
#甚至可以操作两个以上的进程内的对象
import rpyc

def main():
    from rpyc.utils.server import ThreadedServer
    t = ThreadedServer(MyService, port = 18861)
    t.start()

class MyService(rpyc.Service):
    def exposed_line_counter(self, fileobj, function):
        print('Client has invoked exposed_line_counter()')
        for linenum, line in enumerate(fileobj.readlines()):
            function(line)
        return linenum + 1

if __name__ == '__main__':
    main()
