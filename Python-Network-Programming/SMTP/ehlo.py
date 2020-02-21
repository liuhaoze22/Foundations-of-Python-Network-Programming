#事先了解远程SMTP服务器能接受的信息类型是有有帮助的，例如大多数服务器对允许接收的消息大小有限制，可以事先检查
#从EHLO获取信息
import smtplib, socket, sys

message_template = """To: {}
From: {}
Subject: Test Message from simple.py

Hello,

What a wonderful world!
"""

def main():
    if len(sys.argv) < 4:
        name = sys.argv[0]
        print("usage: {} server fromaddr toaddr [toaddr...]".format(name))
        sys.exit(2)

    server, fromaddr, toaddrs = sys.argv[1], sys.argv[2], sys.argv[3:]
    message = message_template.format(', '.join(toaddrs), fromaddr)

    try:
        connection = smtplib.SMTP(server)
        report_on_message_size(connection, fromaddr, toaddrs, message)
    except (socket.gaierror, socket.error, socket.herror,
            smtplib.SMTPException) as e:
        print("Your message may not have been sent!")
        print(e)
        sys.exit(1)
    else:
        s = '' if len(toaddrs) == 1 else 's'
        print("Message sent to {} recipient{}".format(len(toaddrs), s))
        connection.quit()

def report_on_message_size(connection, fromaddr, toaddrs, message):
    #支持ESMTP的客户端会用EHLO命令,EHLO和HELO会返回两个列表，列表的第一项是由远程服务器返回一个由数字表示的结果代码
    #200-299表示成功
    code = connection.ehlo()[0]
    uses_esmtp = (200 <= code <= 299)
    #如果不支持ESMTP，则使用helo命令作为会话的起始命令
    if not uses_esmtp:
        code = connection.helo()[0]
        if not (200 <= code <= 299):
            print("Remote server refused HELO; code:", code)
            sys.exit(1)
    #has_extn()返回True如果名称是在设置服务器返回的SMTP服务扩展的
    if uses_esmtp and connection.has_extn('size'):
        print("Maximum message size is", connection.esmtp_features['size'])
        if len(message) > int(connection.esmtp_features['size']):
            print("Message too large; aborting.")
            sys.exit(1)

    connection.sendmail(fromaddr, toaddrs, message)

if __name__ == '__main__':
    main()