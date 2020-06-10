import  requests
import logging

# 定义一个函数，来实现 http get 的方法
def httpClientGet():
    '''
    函数模拟请求网站首页，然后将 http 响应头部请求，http 响应状态码及 响应报文都打印输出
    '''

    response = requests.get( 'http://www.baidu.com')
    if response.status_code != 200 :
        raise
    # 打印输出 http 状态码
    print( response.status_code)

    # 打印输出 http 的响应头部及指定头部参数输出
    print( response.headers)
    print( response.headers['Content-Type'])

    # 打印输出 http 响应报文结构
    print( response.text)

if __name__ == '__main__' :
    httpClientGet()
