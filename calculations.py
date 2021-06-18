import operator as op
from time import localtime
from itertools import groupby
import metrics
import datetime

index = -1


def remove_yesterday_data(db, dates):
    result = []
    for day in db:
        if day['DATE'] > datetime.datetime.strptime(dates['finish'], '%m.%d.%Y').timestamp() * 1000:
            result.append(day)
    return result


def get_sorted_data(data, key):
    parsed = data
    parsed.sort(key=op.itemgetter(key))
    return parsed


def get_metric(data: list, dates):
    data = remove_yesterday_data(data, dates)
    group_db = get_groups_bd(data)
    metric = metrics.get_metrics(group_db)
    return metric


# Возвращает словарь ключ - дата(день, месяц, год), значение - список записей бд за этот месяц
def get_groups_bd(bd):
    data_base_sort_time = add_time_dd_mm_yyyy(get_sorted_data(bd, 'DATE'))
    print(111, data_base_sort_time)
    groups_list_bd = {}
    for i, action in groupby(data_base_sort_time, lambda x: x['DATE_DD_MM_YYYY']):
        order_action = sorted(action, key=lambda x: x['INN'])
        groups_list_bd[i] = order_action
    return groups_list_bd


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
        day_metric[date] = metrics.get_metrics({date: group})
    return day_metric


def get_full_metric(dict_day_metrics: dict):
    metrics_sum = 0
    count_day = 0
    for day, metric in dict_day_metrics.items():
        count_day += 1
        metrics_sum += metric
    return metrics_sum / count_day
