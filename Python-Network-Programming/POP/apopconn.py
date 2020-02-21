#有时POP服务器不支持通过SSL来保护连接不被窃听，但是这些服务器至少会支持一个APOP认证协议
#例：apopconn.py mail.example.com brandon
import getpass, poplib, sys

def main():
    if len(sys.argv) != 3:
        print('usage: %s hostname username' % sys.argv[0])
        exit(2)

    hostname, username = sys.argv[1:]
    passwd = getpass.getpass()

    p = poplib.POP3_SSL(hostname)  # or "POP3" if SSL is not supported
    try:
        #尝试使用APOP
        p.apop(username, passwd)
    except poplib.error_proto as e:
        print("Login failed:", e)
    else:
        status = p.stat()
        print("You have %d messages totaling %d bytes" % status)
    finally:
        p.quit()

if __name__ == '__main__':
    main()
