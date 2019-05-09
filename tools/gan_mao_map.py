# -*- coding: utf-8 -*-
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.naive_bayes import GaussianNB

te_map = {
    "风寒感冒": ["鼻塞", "声重", "喷嚏", "流清涕", "恶寒", "全身酸痛",
               "咳嗽", "痰白质稀", "舌苔薄白", "脉浮紧",
               "微热"],
    "风热感冒": ["鼻塞", "喷嚏", "流稠涕", "发热", "高热", "咳嗽",
               "痰稠", "舌苔薄黄", "脉浮数", "出汗", "咽痛", "微恶风",
               "口干"],
    "暑湿感冒": ["发热", "出汗", "鼻塞", "流稠涕", "头昏",
               "头痛", "胀痛", "乏力", "心烦", "口渴", "胸闷",
               "欲呕", "尿短", "尿赤", "舌苔黄腻", "脉濡数"],
    "表寒里热感冒": ["发热", "恶寒", "无汗", "口渴", "鼻塞", "声重", "咽痛",
                  "咳嗽", "气急", "痰黄粘稠", "尿赤", "便秘",
                  "舌苔黄白相兼", "脉浮数"],
    "时行感冒": ["高热", "全身症状重", "体温39-40度", "全身酸痛", "鼻塞",
               "流涕", "咽痛", "干咳", "咳血", "气急", "唇甲青紫",
               "头昏", "惊厥"],
    "气虚感冒": ["恶寒重", "微热", "鼻塞", "流涕", "头痛", "无汗",
               "乏力", "咳嗽", "咳痰无力", "舌苔薄白淡", "脉浮"],
    "阴虚感冒": ["身热", "手足心热", "微恶寒", "少汗", "头昏", "心烦",
               "口干", "干咳", "少痰", "鼻塞", "流涕", "舌红少苔", "脉细数"]
}

jie_map = {
    "风寒感冒": {"title": "荆防败毒散", "content": "荆芥、防风、羌活、独活各10g，柴胡、前胡、川芎、枳壳、茯苓、桔梗各6g，甘草3g。将所有药材研为细末，每次取6g，用水煎煮后服用。",
               "other": "午时茶，通宣理肺丸"},
    "风热感冒": {"title": "银翘散", "content": "连翘30克 银花30克 苦桔梗18克 薄荷18克 竹叶12克 生甘草15克 芥穗12克 淡豆豉15克 牛蒡子18克"},
    "暑湿感冒": {"title": "新加香薷饮", "content": "香薷6克（二钱），银花9克（三钱），鲜扁豆花9克（三钱），厚朴6克（二钱），连翘6克（二钱）。水煎服"},
    "表寒里热感冒": {"title": "双解汤", "content": "薄荷6g，荆芥3g，桑皮9g，银花18g，酒黄芩12g，石膏12g，酒大黄6g，赤芍9g，牡丹皮6g"},
    "时行感冒": {"title": "荆防败毒散+银翘散+新加香薷饮", "content": "",
               "other": "板蓝根, 西药"},
    "气虚感冒": {"title": "参苏饮", "content": "人参6g，紫苏叶6g，葛根6g、半夏6g、前胡6g、茯苓6g、枳壳4g、木香4g、陈皮4g、甘草4g、桔梗4g。加生姜7片，大枣1枚，水煎温服。"},
    "阴虚感冒": {"title": "加减葳蕤汤", "content": "生葳蕤、淡豆豉各9g，红枣二枚，生葱白6g，炙甘草1.5g，桔梗、苏薄荷各5g，东白薇3g。水煎，分温再服。"},
}

zz = {}

maxz = 0

for k, v in te_map.items():
    ll = len(v)
    if ll > maxz:
        maxz = ll
    for i in v:
        zz[i] = zz.get(i, 0) + 1

l_k = len(zz.keys())

# print(zz)
# print(l_k)
# print(maxz)

# dd = sorted(zz.keys())

# ll = sorted(zz.items(), key=lambda x: x[1])

# print(ll)
# print(dd)

vectorizer = HashingVectorizer(n_features=l_k)


zheng_chuang_map = {k: v for k, v in enumerate(zz.keys())}

map_zheng_chuang = {v: k for k, v in zheng_chuang_map.items()}

# print(zheng_chuang_map)

# print(map_zheng_chuang)

type_map = {k: v for k, v in enumerate(te_map.keys())}

# print(type_map)

map_type = {v: k for k, v in enumerate(te_map.keys())}

# print(map_type)

"""
te_map_shu = {}

for k, v in te_map.items():
    list1 = []
    for i in v:
        list1.append(map_zheng_chuang.get(i, 99))

    # while len(list1) != maxz:
    #     list1.append(-1)

    te_map_shu[map_type.get(k, 99)] = list1

print(te_map_shu)
"""

x = []
y = []

for k, v in te_map.items():
    x.append(vectorizer.transform([" ".join(v)]).toarray()[0])
    y.append(map_type[k])

# print(x)
# print(y)

clf = GaussianNB()

clf.fit(x, y)


def toTest(list1):
    vector = vectorizer.transform([" ".join(list1)])
    return clf.predict(vector.toarray()), clf.predict_proba(vector.toarray())
