#解析电子邮件信息

#示例：
#build_mime_email.py > email.txt
#display_email.py email.txt

import argparse, email.policy, sys

def main(binary_file):
    policy = email.policy.SMTP
    #从打开的二进制文件对象返回消息对象结构树
    message = email.message_from_binary_file(binary_file, policy=policy)
    for header in ['From', 'To', 'Date', 'Subject']:
        print(header + ':', message.get(header, '(none)'))
    print()

    try:
        #返回最适合作为邮件 “正文”的MIME部分
        body = message.get_body(preferencelist=('plain', 'html'))
    except KeyError:
        print('<This message lacks a printable text or HTML body>')
    else:
        print(body.get_content())

    #该walk()方法是一个通用生成器，可用于按深度优先的遍历顺序遍历消息对象树的所有部分和子部分。
    #您通常会walk()在for循环中用作迭代器；每次迭代都会返回下一个子部分。
    for part in message.walk():
        #如果有附加的文件显示出来
        cd = part['Content-Disposition']
        is_attachment = cd and cd.split(';')[0].lower() == 'attachment'
        if not is_attachment:
            continue
        content = part.get_content()
        print('* {} attachment named {!r}: {} object of length {}'.format(
            part.get_content_type(), part.get_filename(), type(content).__name__, len(content)))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parse and print an email')
    parser.add_argument('filename', nargs='?', help='File containing an email')
    args = parser.parse_args()
    if args.filename is None:
        main(sys.stdin.buffer)
    else:
        with open(args.filename, 'rb') as f:
            main(f)