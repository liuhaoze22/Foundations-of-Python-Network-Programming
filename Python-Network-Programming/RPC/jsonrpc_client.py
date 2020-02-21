
from jsonrpclib import Server

def main():
    proxy = Server('http://localhost:7002')
    print(proxy.lengths((1,2,3), 27, {'Sirius': -1.46, 'Rigel': 0.12}))

if __name__ == '__main__':
    main()
