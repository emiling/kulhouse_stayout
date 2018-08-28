import datetime
from urllib.parse import quote
import aiohttp
import asyncio
import configparser
from bs4 import BeautifulSoup

headers = []

url = "https://kulhouse.konkuk.ac.kr"
login_url = url + "/home/login/login_ok.asp"
info_url = url+ "/home/sub06/mypage00.asp"
stayout_url = url + "/home/sub06/mypage00_01_proc.asp"

header = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}


class Kuluser() :

    def __init__(self):

        self.login_payload = {
            'std_no': "",
            'pwd': "",
            'mode': 'user',
            'url': quote(info_url)
        }

        self.parseIni()
        self.login_payload['std_no'] = self.id
        self.login_payload['pwd'] = self.pwd

        self.stayout_payload = {
            'id_no': '',
            'recruit_year': '2018',
            'recruit_code': '2602000',
            'recruit': '2018,2602000,2018-08-20 ~ 2019-02-19',
            'std_no': '201711413',
            'user_nm': quote(''),
            'sleep_cnt': '0',
            'rec_cnt': '0',
            'ov_reason': '1101001',
            'sdate': '',
            'edate': '',
            'memo': quote('I am groot')
        }


    def parseIni(self) :
        config = configparser.ConfigParser()
        config.read('config.ini', encoding='UTF-8')

        self.id = config['KULHOUSE']['client_stdnum']
        self.pwd = config['KULHOUSE']['client_password']


    def get_info(self, login_response):
        soup = BeautifulSoup(login_response, 'html.parser')

        id_no1 = soup.find('input', {'name': 'id_no1'}).get('value')
        id_no2 = soup.find('input', {'name': 'id_no2'}).get('value')
        id_no = id_no1 + id_no2

        user_nm = soup.find('input', {'name': 'user_nm'}).get('value')

        self.stayout_payload['id_no'] = id_no
        self.stayout_payload['user_nm'] = quote(user_nm)



async def apply_stayout(sdate, edate):
    async with aiohttp.ClientSession() as session:

        user = Kuluser()

        async with session.post(login_url, data=user.login_payload, headers=header) as login_response:
            async with session.get(info_url, headers=header) as response :
                user.get_info(await response.text())

        user.stayout_payload['sdate'] = sdate
        user.stayout_payload['edate'] = edate

        async with session.post(stayout_url, data=user.stayout_payload, headers=header) as response:
            result = await response.text()
            print("{sdate}부터 {edate}까지 신청이 완료 되었습니다\n".format(sdate=sdate, edate=edate))


loop = asyncio.get_event_loop()

tasks = []

start = datetime.datetime(year=2018, month=8, day=24)
day = start
final = datetime.datetime(year=2019, month=2, day=19)


while (day < final):
    sdate = day.strftime("%Y-%m-%d")
    edate = (day + datetime.timedelta(days=2)).strftime("%Y-%m-%d")

    task = asyncio.ensure_future(apply_stayout(sdate, edate))
    tasks.append(task)

    day = day + datetime.timedelta(days=7)

loop.run_until_complete(asyncio.wait(tasks))