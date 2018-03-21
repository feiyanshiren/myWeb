# -*- coding: utf-8 -*-
"""
配置文件
"""
#设置环境
import time
#import pymongo
#import redis

#配置
#数据库ip地址
# db_ip = "127.0.0.1"
#db_ip = "211.149.172.120"
db_ip = "192.168.0.114"
#数据库端口
db_port = 22222
# db_port = 27017
#数据库名
db_name = "mds"
#数据库用户名
# db_user = ""
db_user = "qianqi"
#db_user = ""
#数据库密码
db_pwd = "qianqimongodb"
#其他端口（备用）
port = 6488

mysql_port = 3306

mysql_user = "root"

mysql_passwd = 'qianqiqianqi'

main_path = ""

#连接数据库
"""
_connection = None
if db_user == "":
    _connection = pymongo.MongoClient(
                        "mongodb://" + db_ip + ":" + str(db_port))
else:
    _connection = pymongo.MongoClient(
    "mongodb://" + db_user + ":" + db_pwd + "@" + db_ip + ":" + str(db_port))
db = _connection[db_name]
"""

#连接数据库
#db_redis = redis.Redis()


#下发命令
def saveToSend(db, sn, user, key, msg, cmd, other):
    """
        数据库保存并发出到腰挂设备函数
        db = 数据库
        sn = 腰挂设备编号
        user = 用户id
        key = 腰挂端数据库表明
        msg = 发送的消息
        cmd = sql语句
        other = lua语句
    """
    msg1 = {}
    msg1["time"] = long(time.time() * 1000)
    msg1["msg"] = msg
    msg1["user"] = user
    msg1["cmd"] = cmd
    msg1["sn"] = sn
    msg1["sendFlag"] = "send"
    msg1["key"] = key
    msg1["other"] = other
    db.msg.save(msg1)

    msg2 = {}
    msg2["cmd"] = "msg"
    msg2["type"] = "send"
    msg2["data"] = msg1
    db.msghistory.save(msg2)
