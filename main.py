import json

from variable import *
from 变量存储与加载 import varLD
from path import *
import requests

class csuLibrary():

    def __init__(self):
        self.session = requests.session()
        self.username = "8209180334"
        self.pwd = "294633"
        self.area = "53" #新校谋区的编号
        self.segment = ''
        self.seatListFun={}

    # 登录，获取一个验证id，这个id将会用于获取token
    def login(self):

        # 登录，获取一个验证id，这个id将会用于获取token

        checkUrl = 'http://libzw.csu.edu.cn/Api/auto_user_check?' + 'user=8209180334&p=b87ccdc40713b8d1c5b37634a7dad9c0&callback=http://libzw.csu.edu.cn/web/seat3?area='+self.area

        reqToken = self.session.get(url=checkUrl)

    def getSegment(self):
        day, hour, minute = getNow()

        url = 'http://libzw.csu.edu.cn/api.php/space_time_buckets?day='+day+'&area='+self.area
        print(url)
        seatHeader2 = getHeader('reqFile/reqSeat2')

        spaceReq = self.session.get(url=url, headers=seatHeader2)
        s = spaceReq.text
        import json
        j = json.loads(s)
        timel = j['data']['list']
        self.segment = str(timel[0]['id'])
        return timel




    # 目前固定了铁道2楼的url， 返回目前的空闲位置
    def checkRest(self):
        day, hour, minute = getNow()
        # 这里是参数，固定了铁道2楼就是这个
        # self.getSegment()
        # print(self.segment)
        spaceUrl = 'http://libzw.csu.edu.cn/api.php/spaces_old?area='+self.area+'&segment='+self.segment+'&day=' + day + '&startTime=' + str(hour) + ':' + str(minute) + '&endTime=22%3A00'
        seatHeader2 = getHeader('reqFile/reqSeat2')

        spaceReq = self.session.get(url=spaceUrl, headers=seatHeader2)
        s = spaceReq.text
        import json
        j = json.loads(s)
        seatList = j['data']['list']
        # print(j)

        rest = {}
        for i in seatList:
            state = i['status_name']
            name = i['name']
            if state == '空闲':
                rest[name] = i['id']
            # if name == 'TF2A014':
            #     print(i['status_name'], i['name'], i, end='\n\n')

        self.seatListFun = rest
        return rest



    # 传入座位id， 选择座位
    def chooseSeat(self, id):

        formData = {}
        formData['access_token'] = self.session.cookies['access_token']
        formData['userid'] = self.session.cookies['userid']

        formData['segment'] = '1519031'
        formData['type'] = str(1)
        seatUrl  = 'http://libzw.csu.edu.cn/api.php/spaces/' +str(id)+ '/book'
        print(seatUrl)
        h = getHeader('reqFile/chooseReq')
        day, hour, minute = getNow()

        h['Referer'] = 'http://libzw.csu.edu.cn/web/seat3?area='+self.area+'&segment='+self.segment+'&day=' + day + '&startTime=' + str(hour) + ':' + str(minute) + '&endTime=22%3A00'
        r = self.session.post(url = seatUrl, headers =h, data=formData)
        return json.loads(r.text)

    def saveCookies(self):
        varLD.saveData(data=self.session.cookies, filePath=FileDir+ '/' + self.username+'cookies')

    def loadCookies(self):
        self.session.cookies = varLD.loadData(filePath=FileDir+ '/' + self.username+'cookies')

if __name__ == '__main__':
    csu = csuLibrary()
    csu.getSegment()
    print(csu.segment)

    if False:  # 是否需要获取新的token
        csu.login()
        print(csu.session.cookies)
        csu.saveCookies()

    else:
        csu.loadCookies()


    # # 获取segment，也就是今天的时间标记, 必须的
    # for i in range(1,100):
    #     csu.area = str(i)
    #     #获取空闲位子
    #     try:
    #         print()
    #         rest = csu.checkRest()
    #         print(csu.area+'空闲的位子有')
    #         for i in rest:
    #             print(i)
    #
    #     except Exception as e:
    #         print(end='')
    #
    #         # print(e)


    rest = csu.checkRest()
    id = rest['XF4E013']
    choose = csu.chooseSeat(id)
    print(choose)




    csu.saveCookies()