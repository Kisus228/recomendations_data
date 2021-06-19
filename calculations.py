import operator as op
from time import localtime
from itertools import groupby
import metrics
import datetime


def get_metric(data: list, day):
    data = remove_yesterday_data(data, day)
    group_db = get_groups_bd(data)
    metric = metrics.get_metrics(group_db)
    return metric


def remove_yesterday_data(db, dates):
    result = []
    for day in db:
        if day['DATE'] < datetime.datetime.strptime(dates, '%m.%d.%Y').timestamp() * 1000:
            result.append(day)
    return result


# Возвращает словарь ключ - дата(день, месяц, год), значение - список записей бд за этот месяц
def get_groups_bd(bd):
    data_base_sort_time = add_time_dd_mm_yyyy(get_sorted_data(bd, 'DATE'))
    groups_list_bd = {}
    for i, action in groupby(data_base_sort_time, lambda x: x['DATE_DD_MM_YYYY']):
        order_action = sorted(action, key=lambda x: x['INN'])
        groups_list_bd[i] = order_action
    return groups_list_bd


def get_sorted_data(data, key):
    parsed = data
    parsed.sort(key=op.itemgetter(key))
    return parsed


# добавляет значение даты(день, месяц, год) в запись
def add_time_dd_mm_yyyy(bd):
    for e in bd:
        lt = localtime(int(e['DATE'])/1000)
        e['DATE_DD_MM_YYYY'] = f'{lt.tm_mday}.{lt.tm_mon}.{lt.tm_year}'
    return bd

