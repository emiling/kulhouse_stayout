import datetime
from urllib.parse import quote
import aiohttp
import asyncio
import configparser

url = "https://kulhouse.konkuk.ac.kr"
login_url = url + "/home/login/login_ok.asp"
stayout_url = url + "/home/sub06/mypage00_01_proc.asp"


config = configparser.ConfigParser()
print(config.read('config.ini', encoding='UTF-8'))

id = config['KULHOUSE']['client_stdnum']
pw = config['KULHOUSE']['client_password']

login_payload = {
    'std_no': id,
    'pwd': pw,
    'mode': 'user',
    'url': quote('https://kulhouse.konkuk.ac.kr/home/sub06/mypage00.asp')
}

login_header = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': ''
}

stayout_payload = {
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

stayout_header = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': ''
}


async def apply_stayout(sdate, edate):
    async with aiohttp.ClientSession() as session:
        async with session.post(login_url, data=login_payload, headers=login_header) as response:
            login_result = await response.text()

        stayout_payload['sdate'] = sdate
        stayout_payload['edate'] = edate

        async with session.post(stayout_url, data=stayout_payload, headers=stayout_header) as response:
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

