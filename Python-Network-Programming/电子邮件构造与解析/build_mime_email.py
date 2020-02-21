#使用MIME标准构造电子邮件，为非ASCII码值提供通用可扩展方案
#示例输入
#build_mime_email.py
#build_mime_email.py attachment.txt attachment.gz
#build_mime_email.py -i
#build_mime_email.py -i attachment.txt attachment.gz

import argparse, email.message, email.policy, email.utils, mimetypes, sys

plain = """Hello,
This is a MIME message.
- LiuHaoZe"""

html = """<p>Hello,</p>
<p>This is a <b>test message</b> from liuhaze.</p>
<p>- <i>liuhaze</i></p>"""

img = """<p>This is the smallest possible blue GIF:</p>
<img src="cid:{}" height="80" width="80">"""

# Tiny example GIF from http://www.perlmonks.org/?node_id=7974
blue_dot = (b'GIF89a1010\x900000\xff000,000010100\x02\x02\x0410;'
            .replace(b'0', b'\x00').replace(b'1', b'\x01'))

def main(args):
    #EmailMessage类python提供用于构造电子邮件信息的最基本的接口
    message = email.message.EmailMessage(email.policy.SMTP)
    message['To'] = 'Test Recipient <recipient@example.com>'
    message['From'] = 'Test Sender <sender@example.com>'
    message['Subject'] = 'Foundations of Python Network Programming'
    #返回本地时间作为已知的日期时间对象。
    message['Date'] = email.utils.formatdate(localtime=True)
    #email.utils.make_msgid(idstring = None，domain = None)返回适合 符合RFC 2822的 Message-ID标头。
    message['Message-ID'] = email.utils.make_msgid()

    if not args.i:
        #set_content()用来设置消息主体
        message.set_content(html, subtype='html')
        message.add_alternative(plain)
    else:
        cid = email.utils.make_msgid()
        message.set_content(html + img.format(cid.strip('<>')), subtype='html')
        #add_related()方法用于向主要内容添加生成消息所用的其他资源。通常主要内容为HTML，并且需要图片，css，javascript时会使用此方法
        message.add_related(blue_dot, 'image', 'gif', cid=cid, filename='blue-dot.gif')
        #以下方法提供其他格式的电子邮件信息
        message.add_alternative(plain)

    for filename in args.filename:
        #根据文件名，路径或URL（由url给出）来猜测文件的类型。返回值是一个元组(type, encoding)
        #其中type是无法猜测的类型（缺少或后缀未知）或形式为的字符串
        mime_type, encoding = mimetypes.guess_type(filename)
        if encoding or (mime_type is None):
            mime_type = 'application/octet-stream'
        main, sub = mime_type.split('/')
        if main == 'text':
            with open(filename, encoding='utf-8') as f:
                text = f.read()
            #以下方法用于提供附件，如PDF文件，图片以及电子表格
            message.add_attachment(text, sub, filename=filename)
        else:
            with open(filename, 'rb') as f:
                data = f.read()
            message.add_attachment(data, main, sub, filename=filename)

    sys.stdout.buffer.write(message.as_bytes())

if __name__ == '__main__':
    parse = argparse.ArgumentParser(description='构建MIME')
    parse.add_argument('-i', action='store_true', help='选择包含GIF图像')
    parse.add_argument('filename', nargs='*', help='尝试发送文件')
    main(parse.parse_args())