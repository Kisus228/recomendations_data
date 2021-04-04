import requests
import json
import operator as op


def createUrlData(url, dates, headers):
    return requests.post(url, json=dates, headers=headers)


def sortAndPrint(data, key):
    parsed = json.loads(data.json())
    parsed.sort(key=op.itemgetter(key))
    for x in parsed:
        print(x)


headers = {"Content-Type": "application/json", "X-Auth-Token": "4CE7B412-49B7-3DCF-B56D-3441B6A3698A"}

url = 'http://localhost:8080/execmodel'

dates = {'start': '01.01.2018', 'finish': '01.02.2018'}

urlData = createUrlData(url, dates, headers)

sortAndPrint(urlData, 'INN')

print(urlData.status_code)
