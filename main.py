import json

from variable import *
from 变量存储与加载 import varLD
from path import *
import requests

class csuLibrary():

    def __init__(self):
        self.session = requests.session()
        self.username = "8209180334"
        self.pwd = "******"


    def login(self):


        data = {
        'appId': 'cascsu',
        "retUrl": "http://libzw.csu.edu.cn/sso/home.php",
        "params":"",
        "openId":"",
        "userId": self.username,
        "password":self.pwd
        }


        headers1 = getHeader(url = 'reqFile/request')

        # for i in headers1:
        #     session.headers[i] = headers1[i]

        url = 'http://libuser.csu.edu.cn/center/ifcuas/login'

        try:
            resp = self.session.post(url = url,  headers = headers1, data = data,allow_redirects=True)
        except Exception as e:
            print('error occur',e)

        # session.cookies['access_token'] = '58eca0ee5625dac2b965f2e378783f5e'
        # print(self.session.cookies)


    def getToken(self):
        home = 'http://libzw.csu.edu.cn/sso/home.php'

        headers2 = getHeader('reqFile/req2')

        homereq = self.session.get(url=home, headers=headers2)


        s = homereq.text
        # print(s)
        import re
        # for i in s:
        #     print(i)
        ans  = re.search('user=.*;', s)
        ans = ans.group()
        ans = ans.replace('";', '')
        ans

        checkUrl = 'http://libzw.csu.edu.cn/Api/auto_user_check?' + ans
        # print(checkUrl)

        reqToken = self.session.get(url=checkUrl)

    # 目前固定了铁道2楼的url
    def checkRest(self):
        day, hour, minute = getNow()
        # 这里是参数，固定了铁道2楼就是这个
        spaceUrl = 'http://libzw.csu.edu.cn/api.php/spaces_old?area=87&segment=1437886&day=' + day + '&startTime=' + str(
            hour) + ':' + str(minute) + '&endTime=22%3A00'

        seatHeader2 = getHeader('reqFile/reqSeat2')

        spaceReq = self.session.get(url=spaceUrl, headers=seatHeader2)
        s = spaceReq.text
        import json
        j = json.loads(s)
        seatList = j['data']['list']

        rest = {}
        for i in seatList:
            state = i['status_name']
            name = i['name']
            if state == '空闲':
                rest[name] = i['id']
            # if name == 'TF2A014':
            #     print(i['status_name'], i['name'], i, end='\n\n')


        return rest


    def chooseSeat(self, id):
        formData = {}
        formData['access_token'] = self.session.cookies['access_token']
        formData['userid'] = self.session.cookies['userid']

        formData['segment'] = '1437886'   # 这里是参数，固定了铁道2楼就是这个
        formData['type'] = str(1)
        seatUrl  = 'http://libzw.csu.edu.cn/api.php/spaces/' +str(id)+ '/book'
        h = getHeader('reqFile/chooseReq')
        r = self.session.post(url = seatUrl, headers =h)
        return json.loads(r.text)

    def saveCookies(self):
        varLD.saveData(data=self.session.cookies, filePath=FileDir+ '/' + self.username+'cookies')

    def loadCookies(self):
        self.session.cookies = varLD.loadData(filePath=FileDir+ '/' + self.username+'cookies')

if __name__ == '__main__':
    csu = csuLibrary()
    flag = 'new1'
    if flag == 'new':
        csu.login()
        csu.getToken()
    else:
        csu.loadCookies()


    rest = csu.checkRest()
    print('空闲的位子有')

    for i in rest:
        print(i)

    print(csu.session.cookies)

    csu.saveCookies()