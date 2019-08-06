# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name ：lc_api
   Description :
   Author : mabin
   date ：2019-8-5
-------------------------------------------------
   Change Activity:
                   2019-8-5:
-------------------------------------------------
"""
import json
import requests
import time
import random
import hashlib
import uuid


class LCAPI(object):
    """
    乐橙平台API基类
    """

    url = 'https://openapi.lechange.cn:443/openapi/{method}'

    app_id = 'lc****************'
    app_secret = '27fcc*************************'

    def request_post(self, method, body):
        """
        post方法请求
        :param method:接口方法
        :param body:传入数据
        :return:
        """
        cur_time = str(int(time.time()))
        nonce = uuid.uuid1().hex
        dict_sort = "time:" + cur_time + ",nonce:" + nonce + ",appSecret:" + self.app_secret
        sign = hashlib.md5(dict_sort.encode()).hexdigest()
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36',
        }

        try:
            sys_dict = {"system": {"ver": "1.0",
                                   "sign": sign,
                                   "appId": self.app_id,
                                   "time": cur_time,
                                   "nonce": nonce},
                        "id": str(random.randint(0, 999999))}
            data = dict(sys_dict, **body)
            response = requests.post(self.url.format(method=method), data=json.dumps(data), headers=header)
            if response.status_code == 200:
                ret = json.loads(response.text)
                result = {
                    "status": 200,
                    "message": ret.get('result')
                }
            else:
                result = {
                    "status": response.status_code,
                    "message": response.reason
                }
        except Exception as e:
            result = {
                "code": 500,
                "message": e.message
            }

        return result


if __name__ == "__main__":
    lc = LCAPI()
    # data为乐橙接口中需要传递的参数
    data = {"params": {
        "token": "At_54d8f08d48124f9eaed0916acd******",
        "deviceId": "5D0****PAJ41F85",

    }}
    # method为乐橙平台接口中的方法名
    method = 'deviceOnline'
    ret = lc.request_post(method, data)
    print ret
    print ret.get('message').get('msg')
