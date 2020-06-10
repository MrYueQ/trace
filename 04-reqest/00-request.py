import  requests

def client():
    resp = requests.get(r'http://www.baidu.com')

    # logging.info('header: {}'.format( resp.headers))
    # logging.info('status code: {}'.format( resp.status_code))
    # 1. 打印 http 头部请求
    print( resp.headers)
    print( resp.headers["Content-Type"])

    # 2. 打印 http 响应状态码
    print( resp.status_code)

    # 3. 打印 http 响应报文
    print( resp.text)

if __name__ == "__main__":
    client()
