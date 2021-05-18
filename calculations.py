import json
import operator as op
import metrics
from time import localtime
from itertools import groupby


def get_sorted_data(data, key):
    # parsed = json.loads(data.json())
    parsed = json.loads(data)
    parsed.sort(key=op.itemgetter(key))
    return parsed


def time_for_people(bd):
    for e in bd:
        lt = localtime(int(e['DATE'])/1000)
        e['DATE'] = f'{lt.tm_mday}.{lt.tm_mon}.{lt.tm_year}  {lt.tm_hour}:{lt.tm_min}:{lt.tm_sec}'
    return bd


def add_time_mm_yyyy(bd):
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
    data_base_sort_time = add_time_mm_yyyy(get_sorted_data(bd, 'DATE'))
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
