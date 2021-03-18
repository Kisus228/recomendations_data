import requests
import json
import operator

headers = {"Content-Type": "application/json", "X-Auth-Token": "4CE7B412-49B7-3DCF-B56D-3441B6A3698A"}


url = 'http://localhost:8080/execmodel'

dates = {'start': '01.01.2018', 'finish': '01.02.2018'}

urlData = requests.post(url, json=dates, headers=headers)

# with open(urlData.json()) as json_file:
#     data = json.load(json_file)
parsed = json.loads(urlData.json())
parsed.sort(key=operator.itemgetter('INN'))
for x in(parsed):
    print(x)
#print(urlData.json())

print(urlData.status_code)