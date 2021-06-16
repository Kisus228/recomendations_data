import operator as op
import metrics
from time import localtime
from itertools import groupby
import random

index = -1


def get_sorted_data(data, key):
    parsed = data
    parsed.sort(key=op.itemgetter(key))
    return parsed


def get_metric(data):
    global index
    dict_day_metric = get_day_metric_dict(get_groups_bd(data))
    list_metric = list(dict_day_metric.values())
    # random_index = random.randint(0, len(list_metric) - 1)
    index += 1
    return list_metric[index]


# добавляет значение даты(день, месяц, год) в запись
def add_time_dd_mm_yyyy(bd):
    for e in bd:
        lt = localtime(int(e['DATE'])/1000)
        e['DATE_DD_MM_YYYY'] = f'{lt.tm_mday}.{lt.tm_mon}.{lt.tm_year}'
    return bd


# возвращает словарь ключ - день, значение - значение метрики за этот день
def get_day_metric_dict(group_db):
    day_metric = {}
    for date, group in group_db.items():
        day_metric[date] = metrics.get_metrics(group)
    return day_metric


# Возвращает словарь ключ - дата(день, месяц, год), значение - список записей бд за этот месяц
def get_groups_bd(bd):
    data_base_sort_time = add_time_dd_mm_yyyy(get_sorted_data(bd, 'DATE'))
    groups_list_bd = {}
    for i, action in groupby(data_base_sort_time, lambda x: x['DATE_DD_MM_YYYY']):
        order_action = sorted(action, key=lambda x: x['INN'])
        groups_list_bd[i] = order_action
    return groups_list_bd


def get_full_metric(dict_day_metrics: dict):
    metrics_sum = 0
    count_day = 0
    for day, metric in dict_day_metrics.items():
        count_day += 1
        metrics_sum += metric
    return metrics_sum / count_day
