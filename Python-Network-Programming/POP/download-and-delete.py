#消息的下载与删除
#例：download-and-delete.py mail.example.com brandon
import email, getpass, poplib, sys

def main():
    if len(sys.argv) != 3:
        print('usage: %s hostname username' % sys.argv[0])
        exit(2)

    hostname, username = sys.argv[1:]
    passwd = getpass.getpass()

    p = poplib.POP3_SSL(hostname)
    try:
        p.user(username)
        p.pass_(passwd)
    except poplib.error_proto as e:
        print("Login failed:", e)
    else:
        visit_all_listings(p)
    finally:
        p.quit()

def visit_all_listings(p):
    response, listings, octets = p.list()
    for listing in listings:
        visit_listing(p, listing)

def visit_listing(p, listing):
    number, size = listing.decode('ascii').split()
    print('Message', number, '(size is', size, 'bytes):')
    print()
    #top()该方法返回值格式与retr()相同，但是不会设置seen标记，只返回消息头以及由body_lines指定的行消息
    response, lines, octets = p.top(number, 0)
    document = '\n'.join( line.decode('ascii') for line in lines )
    message = email.message_from_string(document)
    for header in 'From', 'To', 'Subject', 'Date':
        if header in message:
            print(header + ':', message[header])
    print()
    print('Read this message [ny]?')
    answer = input()
    if answer.lower().startswith('y'):
        #该方法下载一条消息，并返回一个元组。元组包含一个结果码和消息本身。
        response, lines, octets = p.retr(number)
        document = '\n'.join( line.decode('ascii') for line in lines )
        message = email.message_from_string(document)
        print('-' * 72)
        for part in message.walk():
            if part.get_content_type() == 'text/plain':
                print(part.get_payload())
                print('-' * 72)
    print()
    print('Delete this message [ny]?')
    answer = input()
    if answer.lower().startswith('y'):
        #该方法对消息进行标记，表示将从POP服务器删除，并且在当前的POP会话结束时生效
        p.dele(number)
        print('Deleted.')

if __name__ == '__main__':
    main()
