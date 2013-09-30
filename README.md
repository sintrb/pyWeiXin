pyWeiXin
========

Python实现的一套简易基于消息驱动的微信公众平台开发框架.<br />
现在已经正常支持SAE了。<br />
在微信公众账号上设置好你SAE的应用地址地址和Token(默认为'youtoken')就可以做测试。

### 开发
开发主要是对消息处理类的开发，需继承WXHandler，重写事件，在事件中调用wxaccess来获取消息内容已经进行回复等等。<br />
可以看WXHandler进行参考.