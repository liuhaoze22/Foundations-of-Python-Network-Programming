#解析电子邮件域名
#例：输入 python.org 或 iana.org
#
import argparse, dns.resolver

def resolve_hostname(hostname):

    answer = dns.resolver.query(hostname, 'A') #查询域名的 A类型
    if answer.rrset is not None:#rrset返回资源记录集
        for recode in answer:
            print('{}的类型A地址为：{}'.format(hostname, recode.address))
        return

    answer = dns.resolver.query(hostname, 'AAAA')
    if answer.rrset is not None:
        for recode in answer:
            print('{}的类型AAAA地址为：{}'.format(hostname, recode.address))
        return
    print('{}没有A和AAAA记录'.format(hostname))
    try:
        answer = dns.resolver.query(hostname, 'CNAME')
        if answer.rrset is not None:
            recode = answer[0]
            cname = recode.address #别名地址
            print('{}的CNAME存在为：{}'.format(hostname, cname))
            resolve_hostname(cname)
            return
    except dns.resolver.NoAnswer:
        print('错误，此主机{}没有CANAME记录'.format(hostname))

def resolve_email_domain(domain):
    try:
        answer = dns.resolver.query(domain, 'MX', raise_on_no_answer=False) 
    except dns.resolver.NXDOMAIN:
        print('error:no such domain', domain)
        return

    if answer.rrset is not None:
        recodes = sorted(answer, key=lambda recode: recode.preference)#按返回资源集中的优先级进行排序
        for recode in recodes:
            name = recode.exchange.to_text(omit_final_dot=True)#提取主机名称 例如mail.python.org。omit_final_dot=True是把后面的点去掉
            print('优先级：', recode.preference)
            resolve_hostname(name)
    else:
        print('此主机没有MX记录')
        print('尝试去返回其他 A , AAAA, CNAME记录')
        resolve_hostname(domain)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='寻找邮箱ip地址')
    parser.add_argument('domain', help='输入主机名称')
    resolve_email_domain(parser.parse_args().domain)