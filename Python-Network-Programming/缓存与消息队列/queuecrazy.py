#消息队列ØMQ
#需要安装 pip install pyzmp
#本例是用蒙特卡洛估算圆周率
#管道模式(PUSH-PULL):生产者创建消息，然后将消息提交到队列中，消费者从队列中接受消息
#发布者-订阅者模式(PUB-SUB):订阅者可以设置一个过滤器，通过特定的格式限定消息范围。
#请求-响应(REQ-REP):允许我们将成百个客户端请求均匀分布在大量服务器中，除了设置消息队列不用做其他工作
#请求-响应能够在在某台机器上大量运行多个轻量级线程，与数据库客户端和文件服务器连接起来是一种很好的方式
#
import random, threading, time, zmq

B = 32 

#返回二进制数
def ones_and_zeros(digits):
    return bin(random.getrandbits(digits)).lstrip('0b').zfill(digits)

#生成一个长2n的字符串，由0和1组成。奇数位n个字符表示x轴坐标，偶数位字符表示y轴坐标
def bitsource(zcontext, pubsub):
    #发布者-订阅者模式，SUB套接字用于广播消息
    zsock = zcontext.socket(zmq.PUB)
    zsock.bind(pubsub)
    while True:
        bit = ones_and_zeros(B * 2)
        zsock.send_string(bit)
        time.sleep(0.01)

#如果字符串前两位为00，那么x轴y轴坐标一定小于坐标最大值的一半，那么这个点一定在第一向限的四分之一圆内
def always_yes(zcontext, pubsub, pushpull):
    #发布者-订阅者模式，SUB套接字用于接受消息
    in_sock = zcontext.socket(zmq.SUB)
    in_sock.connect(pubsub)
    in_sock.setsockopt(zmq.SUBSCRIBE, b'00')
    #管道模式，PUSH用于广播消息
    out_sock = zcontext.socket(zmq.PUSH)
    out_sock.connect(pushpull)
    while True:
        in_sock.recv_string()
        out_sock.send_string('Y')

#如果字符串前两位为01，10，11需要进行判断是否在圆内
#此模块会请求pythagoras模块，计算两个整数坐标的平方和，然后判断对应的点是否在第一向限内
def judge(zcontext, pubsub, reqrep, pushpull):
    #发布者-订阅者模式，SUB套接字用于接受消息
    in_sock = zcontext.socket(zmq.SUB)
    in_sock.connect(pubsub)
    for prefix in b'01', b'10', b'11':
        in_sock.setsockopt(zmq.SUBSCRIBE, prefix)
    #请求-响应，REQ用于发送
    p_sock = zcontext.socket(zmq.REQ)
    p_sock.connect(reqrep)
    #管道模式，PUSH用于广播消息
    out_sock = zcontext.socket(zmq.PUSH)
    out_sock.connect(pushpull)
    unit = 2 ** (B * 2)
    while True:
        bits = in_sock.recv_string()
        n, m = int(bits[::2], 2), int(bits[1::2], 2)
        p_sock.send_json((n, m))
        sumsquares = p_sock.recv_json()
        out_sock.send_string('Y' if sumsquares < unit else 'N')

def pythagoras(zcontext, reqrep):
    #请求-响应，REP用于接收
    zsock = zcontext.socket(zmq.REP)
    zsock.bind(reqrep)
    while True:
        numbers = zsock.recv_json()
        zsock.send_json(sum(n * n for n in numbers))

def tally(zcontext, pushpull):
    #管道模式，PUSH用于接受队列消息
    zsock = zcontext.socket(zmq.PULL)
    zsock.bind(pushpull)
    p = q = 0
    while True:
        decision = zsock.recv_string()
        q += 1
        if decision == 'Y':
            p += 4
        print(decision, p / q)

def start_thread(function, *args):
    thread = threading.Thread(target=function, args=args)
    thread.daemon = True
    thread.start()

def main(zcontext):
    pubsub = 'tcp://127.0.0.1:6700'
    reqrep = 'tcp://127.0.0.1:6701'
    pushpull = 'tcp://127.0.0.1:6702'
    start_thread(bitsource, zcontext, pubsub)
    start_thread(always_yes, zcontext, pubsub, pushpull)
    start_thread(judge, zcontext, pubsub, reqrep, pushpull)
    start_thread(pythagoras, zcontext, reqrep)
    start_thread(tally, zcontext, pushpull)
    time.sleep(30)

if __name__ == '__main__':
    main(zmq.Context())