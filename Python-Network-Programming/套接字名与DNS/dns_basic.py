#一个简单的DNS询问，DNS需要第三方库 使用pip install dnspython3命令
#A：表示ipv4。AAAA：表示ipv6。NS：名称服务器记录。MX：邮件服务器。CNAME：主机名别名，现在并不流行但也可能会遇到
#例：输入python.org
import dns.resolver
import argparse

def lookup(name):
    for qtype in 'A', 'AAAA', 'NS', 'MX', 'CNAME':
        answer = dns.resolver.query(name, qtype, raise_on_no_answer=False) #对不同记录的类型进行dns查询
        if answer.rrset is not None: #rrset返回资源记录集
            print(answer.rrset)

if __name__  == '__main__':
    parser = argparse.ArgumentParser(description='dns 解析')
    parser.add_argument('name', help='想要连的dns名字')
    args = parser.parse_args()
    lookup(args.name)