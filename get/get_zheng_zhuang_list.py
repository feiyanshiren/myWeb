# -*- coding: utf-8 -*-
import json
from tools import gan_mao_map

def post(self):
    try:
        #获取参数
        list1 = list(gan_mao_map.zz.keys())
        list1.sort()
        return json.dumps(list1, ensure_ascii=False)
    except:
        return '{"code":-1}' 