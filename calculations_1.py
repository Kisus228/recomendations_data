import json
import operator as op
import metrics
from time import localtime
from itertools import groupby


def get_sorted_data(data, key):
    parsed = json.loads(data)
    parsed.sort(key=op.itemgetter(key))
    return parsed


# добавляет значение даты(день, месяц, год) в запись
def add_time_dd_mm_yyyy(bd):
    for e in bd:
        lt = localtime(int(e['DATE'])/1000)
        e['DATE_DD_MM_YYYY'] = f'{lt.tm_mday}.{lt.tm_mon}.{lt.tm_year}'
    return bd


# возвращает словарь ключ - день, значение - значение метрики за этот день
def get_dict_day_metric(group_db):
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


def get_dict_month_metric(dict_day_metric:dict):
    dict_month_metric = {}
    list_metric_for_month = []
    now_month = ''
    for date, metric in dict_day_metric.items():
        date = date.split('.')
        month = f'{date[1]}.{date[2]}'
        if now_month == month:
            list_metric_for_month.append(metric)
        else:
            if now_month == '':
                now_month = month
                list_metric_for_month.append(metric)
            else:
                dict_month_metric[now_month] = sum(list_metric_for_month) / len(list_metric_for_month)
                list_metric_for_month.clear()
                list_metric_for_month.append(metric)
                now_month = month
    dict_month_metric[now_month] = sum(list_metric_for_month) / len(list_metric_for_month)
    return dict_month_metric


def get_dict_week_metric(dict_day_metric:dict):
    dict_week_metric = {}
    list_metric_for_week = []
    count_day = 0
    count_week = 1
    for date, metric in dict_day_metric.items():
        if count_day == 7:
            dict_week_metric[count_week] = sum(list_metric_for_week) / len(list_metric_for_week)
            count_week += 1
            count_day = 0
        list_metric_for_week.append(metric)
        count_day += 1
    return dict_week_metric


def get_full_metric(dict_day_metrics:dict):
    metrics = 0
    count_day = 0
    for day, metric in dict_day_metrics.items():
        count_day += 1
        metrics += metric
    return metrics/count_day