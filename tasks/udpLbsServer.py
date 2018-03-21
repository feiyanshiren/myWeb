# -*- coding:utf-8 -*-
import socket
import time
import json
import httplib
import threading
import traceback
import datetime
import sys

#更变运行字符环境
reload(sys)  
sys.setdefaultencoding('utf-8')  # @UndefinedVariable




isWrite = False



#500条
class myThread (threading.Thread):
    def __init__(self,msg):
        threading.Thread.__init__(self)
        self.msg = msg
    def run(self): 
        global isWrite
        try:
            while(isWrite):
                pass
            isWrite = True
            document = open("lbs", "r")    
            strData = document.read()
            document.close()
            jstrData = None
            #print(strData)
            
            try:   
                jstrData = json.loads(strData)
            except:
                jstrData = []
            
            lac16 = self.msg[0:4]
            ci16 = self.msg[4:8]
            lac = int(lac16, 16)
            ci = int(ci16, 16)
            url = "http://api.cellocation.com:81/cell/?mcc=460&mnc=1&lac=%d&ci=%d&output=json" % (lac, ci)
            conn = httplib.HTTPConnection("api.cellocation.com:81")
            conn.request(method="GET", url=url)
            response = conn.getresponse()
            res = response.read()
            now = datetime.datetime.now()
            strNow = now.strftime('%Y-%m-%d %H:%M:%S')  
            if len(jstrData) >= 500:
                jstrData.pop(0)
            jres = json.loads(res, encoding="utf-8")
            jres["date"] = strNow
            jstrData.append(jres)
            ss = json.dumps(jstrData, ensure_ascii=False)
            document = open("lbs", "w")
            document.write(ss)
            document.close()
            isWrite = False
        except:
            isWrite = False
            traceback.print_exc()




#address = ('23.88.228.36', 31500)
address = ('0.0.0.0', 31500)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(address)

while True:
    data, addr = s.recvfrom(128)
    if data is not None: 
        #print "received:", data, "from", addr ,"time:",time.time()
        newThread = myThread(data)
        newThread.start()

s.close()

    