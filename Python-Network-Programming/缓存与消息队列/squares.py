#缓存技术
#Memcached意为‘内存缓存守护进程’，目地是将重复计算花销较高的结果记录下来,以此来进行加速。
#安装Memcached
#pip install python3-memcached
#启动
#memcached -d -m 10 -u root -l 0.0.0.0 -p 12000 -c 256 -P /tmp/memcached.pid
import memcache, random, time, timeit

def compute_square(mc, n):
    value = mc.get('sq:%d' % n)
    if value is None:
        time.sleep(0.001) #模仿昂贵操作
        value = n * n
        mc.set('sq:%d' % n, value)
    return value

def main():
    #将所有Memcached守护进程IP地址和端口号列出，并将该列表发送给所有将要使用Memcached的客户端
    mc = memcache.Client(['127.0.0.1:11211'])
    def make_request():
        compute_square(mc, random.randint(0, 5000))

    print('ten successive runs:')
    for i in range(1, 11):
        print(' %.2fs' % timeit.timeit(make_request, number=2000), end='')
    print()

if __name__ == '__main__':
    main()