# -*- coding: UTF-8 -*
'''
Created on 2013-8-31

@author: RobinTang
'''

import re
import sys
import time
import hashlib
from pyxmldict import dict2xml
import xml.etree.ElementTree as ET
try:
	sys.setdefaultencoding("utf-8")
except:
	pass

def xml2dict(xml):
	ret = {}
	tree = ET.XML(xml)
	for child in tree.getchildren():
		ret[child.tag] = str(child.text).strip()
	return ret




def new_articlesmsg(FromUserName, ToUserName, Articles, retxml=True):
	'''
	创建图文回复
	@Articles 图文项数组，每项含：Title、Description、PicUrl、Url
	'''
	dic = {
		'ToUserName':str(ToUserName),
		'FromUserName':str(FromUserName),
		'CreateTime':int(time.time()),
		'MsgType':'news',
		'ArticleCount':len(Articles),
		'Articles':Articles
		}
	if retxml:
		return dict2xml(dic).replace('<Article>', '<item>').replace('</Article>', '</item>')
	else:
		return dic

def new_musicmsg(FromUserName, ToUserName, Title, Description, MusicUrl, HQMusicUrl, retxml=True):
	'''
	创建音乐回复
	'''
	dic = {
		'ToUserName':str(ToUserName),
		'FromUserName':str(FromUserName),
		'CreateTime':int(time.time()),
		'MsgType':'music',
		'Music':{
				'Title':Title,
				'Description':Description,
				'MusicUrl':MusicUrl,
				'HQMusicUrl':HQMusicUrl
				}
		}
	if retxml:
		return dict2xml(dic)
	else:
		return dic

def new_textmsg(FromUserName, ToUserName, Content, retxml=True):
	'''
	创建文本回复
	'''
	dic = {
		'ToUserName':str(ToUserName),
		'FromUserName':str(FromUserName),
		'CreateTime':int(time.time()),
		'MsgType':'text',
		'Content':str(Content)
		}
	if retxml:
		return dict2xml(dic)
	else:
		return dic

class WXAccess(object):
	def __init__(self, parameters=None, postdata=None, accesstoken=None, wxtoken=None):
		self.accesstoken = accesstoken
		self.wxtoken = wxtoken
		self.reqdict = {}
		self.fromuser = ''
		self.touser = ''
		self.msgtype = ''
		self.parameters = {}
		self.postdata = ''
		if parameters:
			self.parameters = parameters
			
		if postdata:
			self.postdata = postdata
			self.reqdict = xml2dict(self.postdata)
			self.fromuser = self.reqdict['FromUserName']
			self.touser = self.reqdict['ToUserName']
			self.msgtype = self.reqdict['MsgType']
	
	def checksignature(self):
		'''
		检查微信服务器提交的Token是否正确
		'''
		signature = self.parameters['signature']
		timestamp = self.parameters['timestamp']
		nonce = self.parameters["nonce"];
		tmparr = [self.wxtoken, timestamp, nonce]
		tmparr.sort()
		tmpstr = ''.join(tmparr)
		tmpstr = hashlib.sha1(tmpstr).hexdigest()
		return tmpstr == signature
	
	def response_checksignature(self):
		'''
		响应验证Token验证，一般在设置公众平台的接口地址的时候用来响应微信服务器的验证
		'''
		if self.checksignature():
			return self.parameters['echostr']
		else:
			return ''

	def response_textmessage(self, message):
		'''
		回复文本信息
		@message 文本消息
		'''
		return new_textmsg(self.touser, self.fromuser, message)
	
	def response_articlesmsg(self, articles):
		'''
		回复图文信息
		@Articles 图文项数组，每项含：Title、Description、PicUrl、Url
		'''
		return new_articlesmsg(self.touser, self.fromuser, articles)
	def response_musicmsg(self, title, description, musicurl, hqmusicurl):
		'''
		回复音乐信息
		@title 标题
		@description 描述
		@musicurl 音乐地址
		@hqmusicurl 高品质的音乐地址（WiFi情况下播放）
		'''
		return new_musicmsg(self.touser, self.fromuser, title, description, musicurl, hqmusicurl)


	# 消息获取
	def get_textmsg(self):
		'''
		获取文本消息
		'''
		return self.reqdict['Content']

	def get_imageurl(self):
		'''
		获取图片地址
		'''
		return self.reqdict['PicUrl']

	def get_locationx(self):
		'''
		获取位置经度
		'''
		return self.reqdict['Location_X']

	def get_locationy(self):
		'''
		获取位置纬度
		'''
		return self.reqdict['Location_Y']

	def get_locationscale(self):
		'''
		获取获取位置缩放
		'''
		return self.reqdict['Scale']

	def get_locationlabel(self):
		'''
		获取位置描述
		'''
		return self.reqdict['Label']

	def get_linktitle(self):
		'''
		获取链接标题
		'''
		return self.reqdict['Title']

	def get_linkdescription(self):
		'''
		获取链接描述
		'''
		return self.reqdict['Description']

	def get_linkurl(self):
		'''
		获取链接地址
		'''
		return self.reqdict['Url']

	def get_mediaid(self):
		'''
		获取获取内容
		'''
		return self.reqdict['MediaId']

	def get_format(self):
		'''
		获取内容格式
		'''
		return self.reqdict['Format']
	
	# 
	def get_echostr(self):
		'''
		获取回显字符串
		'''
		return self.parameters['echostr']
	


class WXHandler(object):
	'''
	处理微信服务器的消息请求
	'''
	test_handler = str
	def __init__(self, accesstoken=None, wxtoken=None):
		self.accesstoken = accesstoken
		self.wxtoken = wxtoken
		self.handlermap = {
						'text': self.whentextmsg,
						'image': self.whenimagemsg,
						'location': self.whenlocationmsg,
						'link': self.whenlinkmsg,
						'voice': self.whenvoicemsg,
 						'video': self.whenvideomsg,
 						'event': self.wheneventmsg
						}


	def whentextmsg(self, wxaccess):
		'''
		用户文本消息事件
		'''
		return wxaccess.response_textmessage('Text\n%s'%wxaccess.get_textmsg())
	
	def whenimagemsg(self, wxaccess):
		'''
		用户图片消息事件
		'''
		return wxaccess.response_textmessage('Image\n url:%s'%wxaccess.get_imageurl())
	
	def whenlocationmsg(self, wxaccess):
		'''
		用户地址消息事件
		'''
		return wxaccess.response_textmessage('Location\nx=%s y=%s sc:%s des:%s' % (wxaccess.get_locationx(), wxaccess.get_locationy(), wxaccess.get_locationscale(), wxaccess.get_locationlabel()))
	
	def whenlinkmsg(self, wxaccess):
		'''
		用户链接消息事件
		'''
		return wxaccess.response_textmessage('Link\ntit:%s url:%s des:%s'%(wxaccess.get_linktitle(), wxaccess.get_linkurl(), wxaccess.get_linkdescription()))

	def whenvoicemsg(self, wxaccess):
		'''
		用户录音消息事件
		'''
		return wxaccess.response_textmessage('Voice\n%s'%wxaccess.get_mediaid())
	
	def whenvideomsg(self, wxaccess):
		'''
		用户视频消息事件
		'''
		return wxaccess.response_textmessage('Video\n%s'%wxaccess.get_mediaid())

	def wheneventmsg(self, wxaccess):
		'''
		消息事件
		'''
		eventtype = wxaccess.reqdict['Event']
		if eventtype == 'subscribe':
			# 订阅
			return self.whensubscribeevent(wxaccess)
		elif eventtype == 'unsubscribe':
			# 取消订阅
			return self.whenunsubscribeevent(wxaccess)
		elif eventtype == 'CLICK':
			# 单击事件
			return self.whenclickevent(wxaccess)
		else:
			return self.whenunknownevent(wxaccess)
	def whensubscribeevent(self, wxaccess):
		'''
		用户添加订阅事件
		'''
		return wxaccess.response_textmessage('欢迎订阅!')
	
	def whenunsubscribeevent(self, wxaccess):
		'''
		用户取消订阅事件
		'''
		return 'default whenunsubscribeevent'
	def whenclickevent(self, wxaccess):
		'''
		用户单击菜单事件
		'''
		return 'default whenclickevent'
	def whenunknownevent(self, wxaccess):
		'''
		未知的事件
		'''
		return 'default whenunknownevent'
	
	
	def whenunknownmsgtype(self, wxaccess):
		'''
		未知的消息类型
		'''
		print '未知的消息类型: %s'%wxaccess.postdata
		return wxaccess.response_textmessage("Unknow Type: %s"%wxaccess.msgtype)
	
	def whenverifytoken(self, wxaccess):
		'''
		验证令牌事件
		'''
		if wxaccess.checksignature():
			return wxaccess.get_echostr()
		else:
			return 'fail'

	def process_request(self, parameters=None, postdata=None, querystr=None):
		'''
		处理微信服务器处理请求
		'''
		if (not parameters or len(parameters)==0) and querystr and len(querystr)>0:
			parameters = dict(re.findall('([^=, ^&, ^?]*)=([^=, ^&]*)', querystr))
		wxaccess = WXAccess(parameters=parameters, postdata=postdata, accesstoken=self.accesstoken, wxtoken=self.wxtoken)
		res = ''
		if postdata and len(postdata) > 0:
			if self.handlermap.has_key(wxaccess.msgtype):
				res = self.handlermap[wxaccess.msgtype](wxaccess)
			else:
				res = self.whenunknownmsgtype(wxaccess)
		else:
			res = self.whenverifytoken(wxaccess)
		return res

def test_handler(hd):
	postdatas = ['''<?xml version="1.0" encoding="utf-8"?>
	<xml> 
		<ToUserName> <![CDATA[toUser]]> </ToUserName>	
		<FromUserName> <![CDATA[fromUser]]> </FromUserName>	
		<CreateTime>1377920346</CreateTime>	
		<MsgType> <![CDATA[text]]> </MsgType>	
		<Content> <![CDATA[哈哈]]> </Content>	
		<MsgId>5918122822563004451</MsgId>
	</xml>
	''',
	'''
	 <xml>
		 <ToUserName><![CDATA[toUser]]></ToUserName>
		 <FromUserName><![CDATA[fromUser]]></FromUserName>
		 <CreateTime>1348831860</CreateTime>
		 <MsgType><![CDATA[image]]></MsgType>
		 <PicUrl><![CDATA[this is a url]]></PicUrl>
		 <MsgId>1234567890123456</MsgId>
	 </xml>
	''',
	'''
	<xml>
		<ToUserName><![CDATA[toUser]]></ToUserName>
		<FromUserName><![CDATA[fromUser]]></FromUserName>
		<CreateTime>1351776360</CreateTime>
		<MsgType><![CDATA[location]]></MsgType>
		<Location_X>23.134521</Location_X>
		<Location_Y>113.358803</Location_Y>
		<Scale>20</Scale>
		<Label><![CDATA[位置信息]]></Label>
		<MsgId>1234567890123456</MsgId>
	</xml> 
	''',
	'''
	<xml>
		<ToUserName><![CDATA[toUser]]></ToUserName>
		<FromUserName><![CDATA[fromUser]]></FromUserName>
		<CreateTime>1351776360</CreateTime>
		<MsgType><![CDATA[link]]></MsgType>
		<Title><![CDATA[公众平台官网链接]]></Title>
		<Description><![CDATA[公众平台官网链接]]></Description>
		<Url><![CDATA[url]]></Url>
		<MsgId>1234567890123456</MsgId>
	</xml>
	''',
	'''
	<xml>
		<ToUserName><![CDATA[toUser]]></ToUserName>
		<FromUserName><![CDATA[FromUser]]></FromUserName>
		<CreateTime>123456789</CreateTime>
		<MsgType><![CDATA[event]]></MsgType>
		<Event><![CDATA[subscribe]]></Event>
		<EventKey><![CDATA[EVENTKEY]]></EventKey>
	</xml>
	''',
	'''
	<xml>
		<ToUserName><![CDATA[gh_9572e3a907db]]></ToUserName>
		<FromUserName><![CDATA[ofYB4jt9Sk0uIY8tv2nrluSH6jcc]]></FromUserName>
		<CreateTime>1380348665</CreateTime>
		<MsgType><![CDATA[event]]></MsgType>
		<Event><![CDATA[subscribe]]></Event>
		<EventKey><![CDATA[]]></EventKey>
	</xml>
	'''
	]
	print hd.process_request(querystr='/api?signature=5a5cdf9834d4194ae799d0a5c91a60d0cbb5c507&echostr=5928508849433613599&timestamp=1379931416&nonce=1380338535')
	for postdata in postdatas:
		print hd.process_request(postdata=postdata)

WXHandler.test_handler = test_handler

if __name__ == '__main__':
	WXHandler.test_handler(WXHandler(wxtoken='bulubulubuluztoken'))

