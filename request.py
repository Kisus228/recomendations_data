import requests
import json
import operator as op
import metrics
import time


def createUrlData(url, dates, headers):
    return requests.post(url, json=dates, headers=headers)


def getSortedData(data, key):
    parsed = json.loads(data.json())
    parsed.sort(key=op.itemgetter(key))
    return parsed


def time_for_people(bd):
    for e in bd:
        lt = time.localtime(int(e['DATE'])/1000)
        e['DATE'] = f'{lt.tm_mday}.{lt.tm_mon}.{lt.tm_year}  {lt.tm_hour}:{lt.tm_min}:{lt.tm_sec}'


headers = {"Content-Type": "application/json", "X-Auth-Token": "4CE7B412-49B7-3DCF-B56D-3441B6A3698A"}

url = 'http://localhost:8080/execmodel'

#dates = {'start': input('Введите дату начала выбоки в формате ДД.ММ.ГГГГ\n'), 'finish': input('Введите дату конца выбоки в формате ДД.ММ.ГГГГ\n')}
dates = {'start': '01.01.2018', 'finish': '01.12.2020'}
urlData = createUrlData(url, dates, headers)

data_base = getSortedData(urlData, 'INN')
time_for_people(data_base)

accuracy = metrics.getMetricks(data_base)
print(accuracy)
print(urlData.status_code)
