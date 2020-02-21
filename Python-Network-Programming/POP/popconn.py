#POP的连接与认证
#例：popconn.py mail.example.com brandon
#   Password abc123
import getpass, poplib, sys
                                                                                         
def main():
    if len(sys.argv) != 3:
        print('usage: %s hostname username' % sys.argv[0])
        exit(2)

    hostname, username = sys.argv[1:]
    passwd = getpass.getpass()
    #创建一个POP3_SSL对象或原始的POP3对象
    p = poplib.POP3_SSL(hostname)  # or "POP3" if SSL is not supported
    try:
        #调用user()和pass_()发送用户名和密码
        p.user(username)
        p.pass_(passwd)
    except poplib.error_proto as e:
        print("Login failed:", e)
    else:
        #连接成功后立刻返回一个简单的元组，其中包含邮箱中的消息数量和消息的总大小
        status = p.stat()
        print("You have %d messages totaling %d bytes" % status)
    finally:
        #最后官不POP连接
        p.quit()

if __name__ == '__main__':
    main()
