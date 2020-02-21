#基础电子邮件解析，只能用原始的ascii文本的形式表示
import email.message, email.policy, email.utils, sys

text = """Hello
The world is so beautiful
-liuhaoze say"""

def main():
    #EmailMessage类python提供用于构造电子邮件信息的最基本的接口
    message = email.message.EmailMessage(email.policy.SMTP)
    message['To'] = 'recipient@example.com'
    message['From'] = 'Test sender <liuhaoze@qq.com>'
    message['Subject'] = 'The Message is what I want to say before I die'
    #返回本地时间作为已知的日期时间对象。
    message['Date'] = email.utils.formatdate(localtime=True)
    #email.utils.make_msgid(idstring = None，domain = None)返回适合 符合RFC 2822的 Message-ID标头。
    message['Message-ID'] = email.utils.make_msgid()
    #调用content_manager的方法，将self作为消息对象传递，并将其他任何参数或关键字作为附加参数传递。
    message.set_content(text)
    #标准输出的缓冲区中写东西
    sys.stdout.buffer.write(message.as_bytes())

if __name__ == '__main__':
    main()