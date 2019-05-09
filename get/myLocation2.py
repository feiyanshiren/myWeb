# -*- coding: utf-8 -*-
import sqlite3
import time
import json

def post(self):
    try:
        #获取参数
        nowTime = long(time.time()*1000)
        config = self.settings['config']
        ss = self.get_argument("str","")
        phone = self.get_argument("phone","")
        cx = sqlite3.connect(config.main_path+"/get/myLocation.db")
        cu = cx.cursor()
        if ss != "":
            cu.execute("insert into location(time,text,other) values(%s, '%s','%s')" %(nowTime,ss,phone))  
            cx.commit()
            cu.close()
            cx.close()
            return
        else:
            cu.execute("select * from location where other='%s' order by time desc"%(phone)) 
            sss = cu.fetchall()
            ddd = []
            for sss1 in sss:
                fff = {}
                tup_birth = time.localtime(sss1[1]/1000)
                format_birth = time.strftime("%Y-%m-%d %H:%M:%S",tup_birth)
                fff["time"] = format_birth
                fff["phone"] = sss1[3]
                jo = json.loads(sss1[2])
                if jo is not None:
                    sss3 = "<a href='http://api.map.baidu.com/marker?location=%s,%s&coord_type=bd09ll&title=当前位置&content=%s&output=html&src=sanyeshu|myLocation3'>地图</a>"%(str(jo.get("lat","0")),str(jo.get("lng","0")),jo.get("location",""))
#                     sss3 = "<a href='http://api.map.baidu.com/geocoder?location=%s,%s&coord_type=bd09ll&output=html&src=sanyeshu|myLocation3'>地图</a>"%(str(jo.get("lat","0")),str(jo.get("lng","0")))
                    fff["map"] = sss3
                    fff["location"] = jo.get("location","")
                    fff["type"] = jo.get("type","") 
                    fff["battery"] = jo.get("battery",-1)          
                ddd.append(fff)
            
            # oldTime  = nowTime - 86400000 
            # cu.execute("delete from location where time < %s"%(oldTime))
            # cx.commit()
            ## 删除大于500条
            cursor = cu.execute("SELECT count(*) from location where other='%s'" % (phone))
            lenss = 0
            for cu1 in cursor:
                lenss = cu1[0]
                break
            ll = lenss - 500
            if ll > 0:
                cu.execute("delete from location where other='%s' and id in (select id from location order by time limit %s)" % (phone, ll))
                cx.commit()
            ##
            
            cu.close()
            cx.close()
            
            strrtn = ""
            for k in ddd:
                strrtn = strrtn + k.get("time","") + " " + k.get("location","")+" "+k.get("map","")+" "+str(k.get("type",0)) +" " + str(k.get("battery",-1)) + "<br />"
            
            return strrtn
    except:
        return '{"code":-1}' 