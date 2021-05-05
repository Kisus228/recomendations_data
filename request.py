import requests
import json
import operator as op
import metrics
from time import localtime
from itertools import groupby


def createUrlData(url, dates, headers):
    return requests.post(url, json=dates, headers=headers)


def getSortedData(data, key):
    parsed = json.loads(data.json())
    parsed.sort(key=op.itemgetter(key))
    return parsed


def time_for_people(bd):
    for e in bd:
        lt = localtime(int(e['DATE'])/1000)
        e['DATE'] = f'{lt.tm_mday}.{lt.tm_mon}.{lt.tm_year}  {lt.tm_hour}:{lt.tm_min}:{lt.tm_sec}'
    return bd


def add_time_mm_gggg(bd):
    for e in bd:
        lt = localtime(int(e['DATE'])/1000)
        e['DATE_MM_YYYY'] = f'{lt.tm_mon}.{lt.tm_year}'
    return bd


def get_dict_month_metric(group_db):
    month_metric = {}
    for date, group in group_db.items():
        month_metric[date] = metrics.get_metrics(group)
    return month_metric


# Возвращает словарь ключ - дата(месяц, год), значение - список записей бд за этот месяц
def get_groups_bd(bd):
    data_base_sort_time = add_time_mm_gggg(getSortedData(bd, 'DATE'))
    groups_list_bd = {}
    for i, action in groupby(data_base_sort_time, lambda x: x['DATE_MM_YYYY']):
        order_action = sorted(action, key=lambda x: x['INN'])
        groups_list_bd[i] = order_action
    return groups_list_bd


def get_full_metric(group_bd, dict_metrics):
    count_line = 0
    metric = 0
    for k, v in group_bd.items():
        l = len(v)
        count_line += l
        metric += l * dict_metrics[k]
    return metric/count_line


headers = {"Content-Type": "application/json", "X-Auth-Token": "4CE7B412-49B7-3DCF-B56D-3441B6A3698A"}
url = 'http://localhost:8080/execmodel'
# dates = {'start': input('Введите дату начала выбоки в формате ММ.ДД.ГГГГ\n'),
#          'finish': input('Введите дату конца выбоки в формате ММ.ДД.ГГГГ\n')}
dates = {'start': '01.01.2018', 'finish': '08.01.2018'}
urlData = createUrlData(url, dates, headers)


group_data_base = get_groups_bd(urlData)
dict_month_metric = get_dict_month_metric(group_data_base)
for date, metric in dict_month_metric.items():
    print(date, metric)
accuracy = get_full_metric(group_data_base, dict_month_metric)
print(accuracy)
print(urlData.status_code)
