#需要SMTP服务器
#示例
#simple.py mail.example.com sender@example.com recipient@example.com
import sys, smtplib, socket

message_template = """To: {}
From: {}
Subject: Test Message from simple.py

Hello,

What a wonderful world!.
"""

def main():
    if len(sys.argv) < 4:
        name = sys.argv[0]
        print("usage: {} server fromaddr toaddr [toaddr...]".format(name))
        sys.exit(2)

    server, fromaddr, toaddrs = sys.argv[1], sys.argv[2], sys.argv[3:]
    message = message_template.format(', '.join(toaddrs), fromaddr)

    try:
        #个实例封装的SMTP连接。它具有支持SMTP和E SMTP操作的全部功能的方法。
        connection = smtplib.SMTP(server)
        #设置调试输出级别。的1或A值True对电平在调试消息结果连接和用于所有消息发送到和从服务器接收的。级别的2 值导致这些消息带有时间戳。
        connection.set_debuglevel(1)
        #发邮件。必需的参数是发件人地址字符串，列表地址字符串（裸字符串将被视为具有1个地址的列表）和消息字符串。
        connection.sendmail(fromaddr, toaddrs, message)
    except (socket.gaierror, socket.error, socket.herror,
            smtplib.SMTPException) as e:
        print("Your message may not have been sent!")
        print(e)
        sys.exit(1)
    else:
        s = '' if len(toaddrs) == 1 else 's'
        print("Message sent to {} recipient{}".format(len(toaddrs), s))
        connection.quit()

if __name__ == '__main__':
    main()