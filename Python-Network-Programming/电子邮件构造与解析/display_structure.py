#手动遍历一个multpart消息所有部件，
#用于可能无法在项目需要解析的电子邮件中找到邮件体本文，也可能因为格式有误而无法获取客户需要的某些部件
#示例：
#build_mime_email.py > email.txt
#display_structure.py email.txt

import argparse, email.policy, sys

def walk(part, prefix=''):
    yield prefix, part
    #enumerate(iterable，start = 0)返回一个枚举对象。iterable必须是序列， 迭代器或其他支持迭代的对象。
    #iter_parts()在消息的所有直接子部分上返回一个迭代器，对于非-子元素将为空multipart
    for i, subpart in enumerate(part.iter_parts()):
        yield from walk(subpart, prefix + '.{}'.format(i))

def main(binary_file):
    policy = email.policy.SMTP
    message = email.message_from_binary_file(binary_file, policy=policy)
    for prefix, part in walk(message):
        line = '{} type={}'.format(prefix, part.get_content_type())
        #is_multipart()用来判断该MIME部件是否包含其他MIME子部件
        if not part.is_multipart():
            #获取MIME部件内的数据并进行解码
            content = part.get_content()
            line += ' {} len={}'.format(type(content).__name__, len(content))
            cd = part['Content-Disposition']
            is_attachment = cd and cd.split(';')[0].lower() == 'attachment'
            if is_attachment:
                line += ' attachment'
            filename = part.get_filename()
            if filename is not None:
                line += ' filename={!r}'.format(filename)
        print(line)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Display MIME structure')
    parser.add_argument('filename', nargs='?', help='File containing an email')
    args = parser.parse_args()
    if args.filename is None:
        main(sys.stdin.buffer)
    else:
        with open(args.filename, 'rb') as f:
            main(f)