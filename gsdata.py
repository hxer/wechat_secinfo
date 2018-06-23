# -*- coding: utf-8 -*-

from itertools import zip_longest
from itertools import chain
from base64 import b64encode
import requests

from config import USER_AGENT


class GSException(Exception):
    pass


class GSData(object):
    def __init__(self):
        self.base_url = 'http://www.gsdata.cn/'
    
    def _encode(self, wx):
        salt = 'QBDSJqing521'
        b64_wx = b64encode(wx.encode('utf-8')).decode('utf-8')
        name = ''.join(chain.from_iterable(zip_longest(b64_wx, salt, fillvalue='')))
        return name.replace('=', 'O0O0O')
    
    def query(self, wx, order=-1):
        wxname = self._encode(wx)
        query_url = '{0}rank/toparc'.format(self.base_url)
        headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': USER_AGENT,
            'Referer': '{0}rank/wxdetail?wxname={1}'.format(self.base_url, wxname)
        }
        params = {
            'wxname': wxname,
            'wx': wx,
            'sort': str(order)
        }
        resp = requests.post(query_url, params=params, headers=headers)
        if resp.status_code != 200:
            raise GSException('connect error: {0}'.format(resp.status_code))
        result = resp.json()
        if result.get('error'):
            """
            {'error': 1, 'error_msg': '禁止访问'} <== 反爬虫策略
            {'error': 1, 'error_msg': '抱歉，该公众号暂无数据'}
            """
            if result.get('error_msg') == '禁止访问':
                raise GSException('response error: 403')
            elif '无数据' in result.get('error_msg'):
                raise GSException('response error: 404')
            else:
                raise GSException('response error: {}'.format(
                        result.get('error_msg')))
        return result['data']




if __name__ == "__main__":
    gs = GSData()

    # print(gs.query('lookvul'))
    # exit(0)
    with open('data.txt', encoding='utf-8') as f:
        for line in f:
            wxname = line.split(' ')[0]
            data = gs.query(wxname)
            for item in data:
                print(
                    item['title'],
                    item['content'],
                    item['url'],
                    item['picurl'],
                    item['name'],
                    item['wx_name'],
                    item['author'],
                    item['readnum_newest'],
                    item['likenum_newest'],
                    item['posttime'],
                    item['add_time']
                )
            break