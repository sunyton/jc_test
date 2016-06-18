#!/usr/lib/python2.7
# -*- coding:utf-8 -*-

import requests
import hashlib
import re
from lxml import etree
import urllib

#模拟登陆需要的数据和加密
username = raw_input("username: ")
password = raw_input("password: ")

m = hashlib.md5()
m.update(password)
login_id = m.hexdigest()
postdata ='$$CDORequest$$=%3CCDO%3E%3CSTRF%20N%3D%22strServiceName%22%20V%3D%22UserService%22%2F%3E%3CSTRF%20N%3D%22strLoginId%22%20V%3D%22'+ username +'%22%2F%3E%3CSTRF%20N%3D%22strTransName%22%20V%3D%22SSOLogin%22%2F%3E%3CSTRF%20N%3D%22strPassword%22%20V%3D%22'+login_id+'%22%2F%3E%3CSTRF%20N%3D%22strVerifyCode%22%20V%3D%22%22%2F%3E%3CSTRF%20N%3D%22bIsCookieLogin%22%20V%3D%22change%22%2F%3E%3CSTRF%20N%3D%22Sessioncheck%22%20V%3D%22sessionErr%22%2F%3E%3CLF%20N%3D%22lSchoolId%22%20V%3D%220%22%2F%3E%3CLF%20N%3D%22lEduId%22%20V%3D%220%22%2F%3E%3C%2FCDO%3E'
url = "http://sso.njcedu.com/handleTrans.cdo?strServiceName=UserService&strTransName=SSOLogin"
headers = {
    "Host": 'sso.njcedu.com',
"Origin": 'http://sso.njcedu.com',
"User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36',
"Content-Type": 'application/x-www-form-urlencoded;charset=UTF-8',
"Accept": '*/*',
"Referer": 'http://sso.njcedu.com/login.htm',
"Accept-Encoding": 'gzip, deflate',
"Accept-Language": 'en,zh;q=0.8,zh-CN;q=0.6,en-US;q=0.4,zh-TW;q=0.2'

}

#requsts登陆，存储cookie

r = requests.post(url=url,headers=headers,data=postdata)

#获取 userid 值
userid = re.search(r'<LF N="lId" V="(\d+)"',r.text)
userid_val = userid.group(1)

#获取cookie中token值
token = r.cookies['token']

#获取 key  值,进一步 获取schooltoken
key = re.search(r'<STR>(.+)</STR>',r.text)
key_val = key.group(1)
print key_val
proxies = {
    "http": 'http://127.0.0.1:8080',
    "https": 'http://127.0.0.1:8080'
}

# 完善cookie，获取 schooltoken 值
cookie = "luserid=" + userid_val + "; token=" + token
headers_sch = {
    "Host": 'yzu.njcedu.com',
"User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36',
"Accept": '*/*',
"Referer": 'http://sso.njcedu.com/login.htm',
"Accept-Encoding": 'gzip, deflate, sdch',
"Accept-Language": 'en,zh;q=0.8,zh-CN;q=0.6,en-US;q=0.4,zh-TW;q=0.2',
}
headers_sch["Cookie"] = cookie
url_sch = key_val + "&jsonpCallback=callback&_=1465879134074"
r_sch = requests.get(url=url_sch,headers=headers_sch)
schooltoken = r_sch.cookies['schoolToken']

cookie = cookie + "; schoolToken=" + schooltoken


#开始对考试惊醒post测试答案
headers_sch["Cookie"] = cookie
headers["Cookie"] = cookie
url_po = "http://yzu.njcedu.com/student/prese/examin/handleTrans.cdo?strServiceName=StudentExminService&strTransName=markStudentExamin"
url_jg = "http://yzu.njcedu.com/student/prese/examin/success.htm?nCommitType=1&lExaminId=10200000057&nExaminType=0"
url_tj = "http://yzu.njcedu.com/student/prese/examin/pager.htm?lId=10200000057&nExaminType=0"
requests.get(url=url_tj,headers=headers_sch)


def csjg():
    r_jg = requests.get(url=url_jg,headers=headers_sch)
    #print r_jg.text
    doc = etree.HTML(r_jg.text)
    v = doc.xpath('/html/body/div[3]/ul/p[1]/span[1]/text()')[0]
    if v == "1":
        return True
    else:
        return False

d_final = ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0',]
def cs(x):
    d = ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0',]
    for d[x] in ['A','B','C','D']:
        if d[x] == "D":
            d_final[x]= "D"
            break
        else:
            d_str = str(d)[2:-2].replace("', '",'%2C')
            test_data = "$$CDORequest$$=%3CCDO%3E%3CSTRF%20N%3D%22%24strDestNodeName%24%22%20V%3D%22TeachingBusiness%22%2F%3E%3CSTRF%20N%3D%22strServiceName%22%20V%3D%22StudentExminService%22%2F%3E%3CSTRF%20N%3D%22strTransName%22%20V%3D%22markStudentExamin%22%2F%3E%3CLF%20N%3D%22lSchoolId%22%20V%3D%22204%22%2F%3E%3CLF%20N%3D%22lUserId%22%20V%3D%22" + userid_val + "%22%2F%3E%3CLF%20N%3D%22lExaminId%22%20V%3D%2210200000057%22%2F%3E%3CLF%20N%3D%22lPlanId%22%20V%3D%2210200000030%22%2F%3E%3CLF%20N%3D%22nExaminType%22%20V%3D%220%22%2F%3E%3CSTRF%20N%3D%22strAnswer0%22%20V%3D%22" + d_str +"%22%2F%3E%3CSTRF%20N%3D%22strAnswer1%22%20V%3D%22%22%2F%3E%3CNF%20N%3D%22nCommitType%22%20V%3D%221%22%2F%3E%3CNF%20N%3D%22nExaminState%22%20V%3D%222%22%2F%3E%3CSTRF%20N%3D%22strToken%22%20V%3D%22%22%2F%3E%3C%2FCDO%3E"
            # print test_data
            requests.post(url=url_po,headers=headers,data=test_data)
            s = csjg()
            # print s
            if s == True:
                d_final[x] = d[x]
                break
    return d_final
sss = 0
while sss < 100:
    cs(sss)
    print sss
    sss = sss + 1
ss_str = str(d_final)[2:-2].replace("', '",'%2C')
print ss_str
test_data2 = "$$CDORequest$$=%3CCDO%3E%3CSTRF%20N%3D%22%24strDestNodeName%24%22%20V%3D%22TeachingBusiness%22%2F%3E%3CSTRF%20N%3D%22strServiceName%22%20V%3D%22StudentExminService%22%2F%3E%3CSTRF%20N%3D%22strTransName%22%20V%3D%22markStudentExamin%22%2F%3E%3CLF%20N%3D%22lSchoolId%22%20V%3D%22204%22%2F%3E%3CLF%20N%3D%22lUserId%22%20V%3D%22" + userid_val + "%22%2F%3E%3CLF%20N%3D%22lExaminId%22%20V%3D%2210200000057%22%2F%3E%3CLF%20N%3D%22lPlanId%22%20V%3D%2210200000030%22%2F%3E%3CLF%20N%3D%22nExaminType%22%20V%3D%220%22%2F%3E%3CSTRF%20N%3D%22strAnswer0%22%20V%3D%22" + ss_str +"%22%2F%3E%3CSTRF%20N%3D%22strAnswer1%22%20V%3D%22%22%2F%3E%3CNF%20N%3D%22nCommitType%22%20V%3D%221%22%2F%3E%3CNF%20N%3D%22nExaminState%22%20V%3D%222%22%2F%3E%3CSTRF%20N%3D%22strToken%22%20V%3D%22%22%2F%3E%3C%2FCDO%3E"
requests.post(url=url_po,headers=headers,data=test_data2)
# r_jg2 = requests.get(url=url_jg,headers=headers_sch)
# doc = etree.HTML(r_jg2.text)
# v = doc.xpath('/html/body/div[3]/ul/p[1]/span[1]/text()')[0]
# print v
