# -*- coding: utf-8 -*-
import json
from tools import gan_mao_map
import traceback
import urllib

def post(self):
    try:
        #获取参数
        ss = self.get_argument("list", "[]")
        ss = urllib.parse.unquote(ss)
        ss = json.loads(ss)
        k, v = gan_mao_map.toTest(ss)
        res_data = {
            "k": int(k[0]),
            "v": list(v[0]),
            "zheng_zhuang": gan_mao_map.type_map[k[0]],
            "fang_an": gan_mao_map.jie_map[gan_mao_map.type_map[k[0]]]
        }
        gl = {}
        for i in range(len(v[0])):
            v1 = v[0][i]
            if v1 > 0.000001:
                gl[gan_mao_map.type_map[i]] = "%.2f%%" % (v1 * 100)
        v_data = {
            "初步诊断": res_data["zheng_zhuang"],
            "病症概率": gl,
            "初步方案": res_data["fang_an"]
        }
        return json.dumps(v_data, ensure_ascii=False)
    except:
        res_data = {"error": traceback.format_exc()}
        return json.dumps(res_data, ensure_ascii=False) 
