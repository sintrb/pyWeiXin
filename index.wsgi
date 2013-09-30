# -*- coding: UTF-8 -*
'''
Created on 2013-9-30

@author: RobinTang
'''

from WeiXin import WXHandler, WXAccess

# 修改wxtoken为你公共帐号设置的Token值
TOKEN = 'youtoken'

# 你可以继承WXHandler，重写事件

wxh = WXHandler(wxtoken = TOKEN)

def app(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type', 'text/xml; charset=utf-8')]
    start_response(status, response_headers)
    s = environ['QUERY_STRING']
    data = environ["wsgi.input"].read() 
    return wxh.process_request(querystr=s, postdata=data)

try:
    import sae
    application = sae.create_wsgi_app(app)
except:
    pass
