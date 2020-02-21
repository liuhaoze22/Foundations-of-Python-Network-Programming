#使用python命令行输入
#python客户端使用urllib和requests来获取页面
#以下使用http://httpbin.org/ 小型网站测试
#pip install gunicorn httpbin requests
#gunicorn httpbin:app

import requests

r = requests.get('http://localhost:8000/headers')
print(r.text)

from urllib.request import urlopen
import  urllib.error

#urllib只会返回原始字节，用户需要自己解码。
r = urlopen('http://localhost:8000/headers')
print(r.read().decode('ascii'))

#重新定向功能，urllib会根据标准为我们提供功能
r = urlopen('http://httpbin.org/status/301')
r.status, r.url
#requests也提供重新定向功能，提供了一个history变量
r = requests.get('http://httpbin.org/status/301')
(r.status_code, r.url)
r.history()
#requests也提供关闭重新定向功能，用一个参数即可：allow_redirects=False
r = requests.get('http://httpbin.org/status/301', allow_redirects=False)
r.raise_for_status()
(r.status_code, r.url, r.headers['Location'])

#以下两个网站对www前缀使用了相反的方案。不过两个网站都使用重新定向将URL转换成官方形式
r = requests.get('http://google.com/')
r.url
r = requests.get('http://www.twitter.com/')
r.url

#如果我们尝试访问的ulr返回了4xx或5xx错误状态码，urlopen()函数会派出一个异常，需要我们去检查异常
urlopen('http://localhost:8000/status/500')

try:
    urlopen('http://localhost:8000/status/500')
except urllib.error.HTTPError as e:
    print(e.status, repr(e.headers['Content-Type']))

#request库不会抛出异常，需要手动检查状态码或者调用r.raise_for_status()函数
r = requests.get('http://localhost:8000/status/500')
r.status_code
r.raise_for_status()

#两个客户端库都允许将Accept头信息加入到请求中，request使用session()来实现
s = requests.Session()
s.headers.update({'Accept-Language': 'en-US, en; q = 0.8'})

#request通过一个参数来支持基本认证
r = requests.get('http://example.com/api/', auth=('brandon', 'atigdngnatwwal'))

#可以事先定义一个session并进行认证，避免每次调用get()或post()时进行重复认证
s = requests.Session()
s.auth = 'brandon', 'atigdngnatwwal'
s.get('http://httpbin.org/basic-auth/brandon/atigdngnatwwal')


