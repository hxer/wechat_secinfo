## 清博大数据微信号加密破解

清博大数据查看公众号详情页链接http://www.gsdata.cn/rank/wxdetail?wxname=bQGBFD6SeJSq1i0nagG59211Z2h0

wxname参数用的并不是微信号或者昵称，看起来是经过了某种处理，第一直觉反应是base64加密了，但是并没有解密出来。通常来说，可以尝试看相近的明文，比较其密文的异同。于是有:

* lazythought -> bQGBFD6SeJXqRionbg35V2n1aHQO0O0O
* lazy-thought -> bQGBFD6SeJSq1i0nagG59211Z2h0

可以看出密文前8个字符相同，但是很奇怪的是明文短的竟然密文要长一些，有些不符合常理，也不是base64的补齐。从密文看不出什么来了，于是根据猜想，看看明文的base64是怎样的

* lazythought -> bGF6eXRob3VnaHQ=
* lazy-thought -> bGF6eS10aG91Z2h0

上下一比较，发现有规律了，密文是在明文base64编码的基础上间隔插入了字符串**QBDSJqing521**，对于base64编码有** = **的，替换成了**O0O0O**

加密代码为

```python3
def _encode(self, wx):
        salt = 'QBDSJqing521'
        b64_wx = b64encode(wx.encode('utf-8')).decode('utf-8')
        name = ''.join(chain.from_iterable(zip_longest(b64_wx, salt, fillvalue='')))
        return name.replace('=', 'O0O0O')
```

## 获取最新发布的文章

获取文章的链接为'http://www.gsdata.cn/rank/toparc?wxname=bQGBFD6SeJSq1i0nagG59211Z2h0&wx=lazy-thought&sort=-1',发送的POST请求，没校验cookies,删除cookies项如下

```
POST /rank/toparc?wxname=bQGBFD6SeJSq1i0nagG59211Z2h0&wx=lazy-thought&sort=-1 HTTP/1.1
Host: www.gsdata.cn
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:59.0) Gecko/20100101 Firefox/59.0
Accept: */*
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Referer: http://www.gsdata.cn/rank/wxdetail?wxname=bQGBFD6SeJSq1i0nagG59211Z2h0
X-Requested-With: XMLHttpRequest
```

得到响应：

```
HTTP/1.1 200 OK
Date: Mon, 09 Apr 2018 12:54:06 GMT
Content-Type: text/html; charset=UTF-8
Connection: keep-alive
Set-Cookie: acw_tc=AQAAAKxTNBrpKgEAY+1Pdz4266TUKo8e; Path=/; HttpOnly
Server: nginx/1.10.0
Content-Length: 3728

{"error":0,"data":[{"copyright":"\u65e0","realreadnum_pm":1,"wx_province":"","type":"49","wx_name":"lazy-thought","nickname_id":560653,"readnum_pm":1975,"author":"\u6162\u96fe\u5b89\u5168\u56e2\u961f","can_reward":0,"picurl":"http:\/\/mmbiz.qpic.cn\/mmbiz_jpg\/kicMePHlP6TDtLia6F0HkAib78iauAoQgomdO7AVad5OvjdZM0dRDiceiba7hdSBr1VhfpuRWcgXBYr5ftB5wcHDvPhw\/0?wx_fmt=jpeg","sourceulr":null,"name":"\u61d2\u4eba\u5728\u601d\u8003","reward_total_count":0,"comment_enabled":"1","wx_city":"","status":"1","posttime":"2018-03-26 19:41:14","posttime_date":"20180326","group_hour":19,"group_week":1,"title":"\u4ee5\u592a\u574a\u9ed1\u8272\u60c5\u4eba\u8282\u4e13\u9898\u4e0a\u7ebf\u53ca\u4e00\u4e9b\u8865\u5145\u89c2\u70b9","top":1,"readnum":1,"sn":"99dc9fb06b0875d6a1525e49a5635f23","types":null,"readnum_newest":3257,"realreadnum_week":3101,"likenum":0,"url":"http:\/\/mp.weixin.qq.com\/s?__biz=MzA3NTEzMTUwNA==&mid=2651081415&idx=1&sn=99dc9fb06b0875d6a1525e49a5635f23&chksm=8485d5d8b3f25cce70bd175d61fd3fc3c55b5b7cdd077a53ce2a84be68491d09603fe538f64c&scene=27#wechat_redirect","readnum_week":3101,"likenum_pm":19,"realreadnum":1,"status_con":"1","likenum_week":29,"likenum_newest":30,"add_time":"2018-03-27 06:33:33","content":"\u7531\u4e8e\u8fd9\u4e2a\u5b89\u5168\u7f3a\u9677\u5bfc\u81f4\u7684\u76d7\u5e01\u4e8b\u4ef6\u6301\u7eed\u4e86\u4e24\u5e74\u4e4b\u4e45\u4e14\u5230\u73b0\u5728\u8fd8\u5728\u6301\u7eed\uff0c\u6d89\u53ca\u7684\u91d1\u989d\u6781\u5176\u5e9e\u5927\uff0c\u6211\u4eec\u56e2\u961f\u4e3a\u6b64\u7279\u610f\u4e0a\u7ebf\u4e86\u4e13\u9898\u9875\u9762\u6765\u8fdb\u884c\u53ca\u65f6\u7684\u5a01\u80c1\u8ffd\u8e2a\u3002","_version_":1596707952891265024,"is_video":null,"is_audio":null,"data-hash":"aHR0cDovL21tYml6LnFwaWMuY24vbW1iaXpfanBnL2tpY01lUEhsUDZURHRMaWE2RjBIa0FpYjc4aWF1QW9RZ29tZE83QVZhZDVPdmpkWk0wZFJEaWNlaWJhN2hkU0JyMVZoZnB1UldjZ1hCWXI1ZnRCNXdjSER2UGh3LzA%2Fd3hfZm10PWpwZWd8Y2I1ZTM2NDkzYTVlY2YwMDMzOWM0ZTc5OTNiNWEyOTg%3D"},{"copyright":"\u65e0","realreadnum_pm":4448,"wx_province":"","type":"49","wx_name":"lazy-thought","nickname_id":560653,"readnum_pm":4448,"author":"","can_reward":0,"picurl":"http:\/\/mmbiz.qpic.cn\/mmbiz_jpg\/qsQ2ibEw5pLaetCPYSJQNjwJtYibY0VhXdgeZwX4Atic1oibOAF3KSArG59bezp1FxD0mpHWIibv4kvc6FaajoJDibQQ\/0?wx_fmt=jpeg","sourceulr":null,"name":"\u61d2\u4eba\u5728\u601d\u8003","reward_total_count":0,"comment_enabled":"1","wx_city":"","status":"1","posttime":"2018-03-20 21:47:54","posttime_date":"20180320","group_hour":21,"group_week":2,"title":"\u4ee5\u592a\u574a\u751f\u6001\u7f3a\u9677\u5bfc\u81f4\u7684\u4e00\u8d77\u4ebf\u7ea7\u4ee3\u5e01\u76d7\u7a83\u5927\u6848","top":1,"readnum":4448,"sn":"5fbff07544ecba1cb713488994e7751e","types":null,"readnum_newest":6420,"realreadnum_week":5920,"likenum":31,"url":"http:\/\/mp.weixin.qq.com\/s?__biz=MzA3NTEzMTUwNA==&mid=2651081408&idx=1&sn=5fbff07544ecba1cb713488994e7751e&chksm=8485d5dfb3f25cc99e1c100c01270e1e08a55feb9f288185d8b59aaeb2e82056f1cacf353366&scene=27#wechat_redirect","readnum_week":5920,"likenum_pm":31,"realreadnum":4448,"status_con":"1","likenum_week":39,"likenum_newest":42,"add_time":"2018-03-21 10:36:00","content":"\u6211\u4eec\u6700\u8fd1\u8ddf\u8fdb\u7684\u4e00\u4e2a\u5927\u6848\u4f8b\uff0c\u7ec6\u601d\u6050\u6781\uff0c\u5927\u5bb6\u8bfb\u5b8c\u540e\uff0c\u53ef\u4ee5\u6269\u5c55\u601d\u8003\u6bd4\u7279\u5e01\u3001\u83b1\u7279\u5e01\u8fd9\u4e9b\u7684\u751f\u6001\u5b89\u5168\u53c8\u662f\u5982\u4f55\uff1f","_version_":1596164530679840768,"is_video":null,"is_audio":null,"data-hash":"aHR0cDovL21tYml6LnFwaWMuY24vbW1iaXpfanBnL3FzUTJpYkV3NXBMYWV0Q1BZU0pRTmp3SnRZaWJZMFZoWGRnZVp3WDRBdGljMW9pYk9BRjNLU0FyRzU5YmV6cDFGeEQwbXBIV0lpYnY0a3ZjNkZhYWpvSkRpYlFRLzA%2Fd3hfZm10PWpwZWd8MjRmNzhlYjkzNzAxODg4NGYyMmIzODY0NzM1NzhhYmU%3D"}]}
```

解析出来

```
{'data': [{'_version_': 1596707952891265024,
   'add_time': '2018-03-27 06:33:33',
   'author': '慢雾安全团队',
   'can_reward': 0,
   'comment_enabled': '1',
   'content': '由于这个安全缺陷导致的盗币事件持续了两年之久且到现在还在持续，涉及的金额极其庞大，我们团队为此特意上线了专题页面来进行及时的威胁追踪。',
   'copyright': '无',
   'data-hash': 'aHR0cDovL21tYml6LnFwaWMuY24vbW1iaXpfanBnL2tpY01lUEhsUDZURHRMaWE2RjBIa0FpYjc4aWF1QW9RZ29tZE83QVZhZDVPdmpkWk0wZFJEaWNlaWJhN2hkU0JyMVZoZnB1UldjZ1hCWXI1ZnRCNXdjSER2UGh3LzA%2Fd3hfZm10PWpwZWd8Y2I1ZTM2NDkzYTVlY2YwMDMzOWM0ZTc5OTNiNWEyOTg%3D',
   'group_hour': 19,
   'group_week': 1,
   'is_audio': None,
   'is_video': None,
   'likenum': 0,
   'likenum_newest': 30,
   'likenum_pm': 19,
   'likenum_week': 29,
   'name': '懒人在思考',
   'nickname_id': 560653,
   'picurl': 'http://mmbiz.qpic.cn/mmbiz_jpg/kicMePHlP6TDtLia6F0HkAib78iauAoQgomdO7AVad5OvjdZM0dRDiceiba7hdSBr1VhfpuRWcgXBYr5ftB5wcHDvPhw/0?wx_fmt=jpeg',
   'posttime': '2018-03-26 19:41:14',
   'posttime_date': '20180326',
   'readnum': 1,
   'readnum_newest': 3257,
   'readnum_pm': 1975,
   'readnum_week': 3101,
   'realreadnum': 1,
   'realreadnum_pm': 1,
   'realreadnum_week': 3101,
   'reward_total_count': 0,
   'sn': '99dc9fb06b0875d6a1525e49a5635f23',
   'sourceulr': None,
   'status': '1',
   'status_con': '1',
   'title': '以太坊黑色情人节专题上线及一些补充观点',
   'top': 1,
   'type': '49',
   'types': None,
   'url': 'http://mp.weixin.qq.com/s?__biz=MzA3NTEzMTUwNA==&mid=2651081415&idx=1&sn=99dc9fb06b0875d6a1525e49a5635f23&chksm=8485d5d8b3f25cce70bd175d61fd3fc3c55b5b7cdd077a53ce2a84be68491d09603fe538f64c&scene=27#wechat_redirect',
   'wx_city': '',
   'wx_name': 'lazy-thought',
   'wx_province': ''},
  {'_version_': 1596164530679840768,
   'add_time': '2018-03-21 10:36:00',
   'author': '',
   'can_reward': 0,
   'comment_enabled': '1',
   'content': '我们最近跟进的一个大案例，细思恐极，大家读完后，可以扩展思考比特币、莱特币这些的生态安全又是如何？',
   'copyright': '无',
   'data-hash': 'aHR0cDovL21tYml6LnFwaWMuY24vbW1iaXpfanBnL3FzUTJpYkV3NXBMYWV0Q1BZU0pRTmp3SnRZaWJZMFZoWGRnZVp3WDRBdGljMW9pYk9BRjNLU0FyRzU5YmV6cDFGeEQwbXBIV0lpYnY0a3ZjNkZhYWpvSkRpYlFRLzA%2Fd3hfZm10PWpwZWd8MjRmNzhlYjkzNzAxODg4NGYyMmIzODY0NzM1NzhhYmU%3D',
   'group_hour': 21,
   'group_week': 2,
   'is_audio': None,
   'is_video': None,
   'likenum': 31,
   'likenum_newest': 42,
   'likenum_pm': 31,
   'likenum_week': 39,
   'name': '懒人在思考',
   'nickname_id': 560653,
   'picurl': 'http://mmbiz.qpic.cn/mmbiz_jpg/qsQ2ibEw5pLaetCPYSJQNjwJtYibY0VhXdgeZwX4Atic1oibOAF3KSArG59bezp1FxD0mpHWIibv4kvc6FaajoJDibQQ/0?wx_fmt=jpeg',
   'posttime': '2018-03-20 21:47:54',
   'posttime_date': '20180320',
   'readnum': 4448,
   'readnum_newest': 6420,
   'readnum_pm': 4448,
   'readnum_week': 5920,
   'realreadnum': 4448,
   'realreadnum_pm': 4448,
   'realreadnum_week': 5920,
   'reward_total_count': 0,
   'sn': '5fbff07544ecba1cb713488994e7751e',
   'sourceulr': None,
   'status': '1',
   'status_con': '1',
   'title': '以太坊生态缺陷导致的一起亿级代币盗窃大案',
   'top': 1,
   'type': '49',
   'types': None,
   'url': 'http://mp.weixin.qq.com/s?__biz=MzA3NTEzMTUwNA==&mid=2651081408&idx=1&sn=5fbff07544ecba1cb713488994e7751e&chksm=8485d5dfb3f25cc99e1c100c01270e1e08a55feb9f288185d8b59aaeb2e82056f1cacf353366&scene=27#wechat_redirect',
   'wx_city': '',
   'wx_name': 'lazy-thought',
   'wx_province': ''}],
 'error': 0}
```
