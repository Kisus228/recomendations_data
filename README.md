# recomendations_data

 При зупуске main файла у вас поднимется сервер на котором хранятся данные за 1 год с 2018 по 2019й, что бы получить данные вам необходимо отправить post зыпрос на адрес 'http://localhost:8080/execmodel', в запросе необходимо передавать значения начальной даты и конечной даты за который вы хотите получить данные.
Пример:{'start': '01.01.2018', 'finish': '01.02.2018'}
Ответ придет в формате {"DATE":1514768835000,"INN":612374057305,"EVENT":"RECOMENDATION"} по каждому событию


Пример запроса полностью:
import requests

headers = {"Content-Type": "application/json", "X-Auth-Token": "4CE7B412-49B7-3DCF-B56D-3441B6A3698A"}
url = 'http://localhost:8080/execmodel'
dates = {'start': '01.01.2018', 'finish': '01.02.2018'}
urlData = requests.post(url, json=dates, headers=headers)
print(urlData.json())
print(urlData.status_code)
