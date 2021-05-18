from time import localtime
import time as tm


def get_recommendation_period_in_seconds(period_in_days):
    return period_in_days * 24 * 3600 * 1000


recommendation_period = 7


def set_recommendation_period(period):
    global recommendation_period
    recommendation_period = get_recommendation_period_in_seconds(period)


def get_actual_events(events):
    set_recommendation_period(7)
    events_by_last_seven_days = []
    for event in events:
        if int(event['DATE']) + recommendation_period >= int(events[len(events) - 1]['DATE']):
            events_by_last_seven_days.append(event)
    return events_by_last_seven_days


def create_groups(data):  # возвращает группы действий по одному инн, т.е. несколько действий одного пользователя
    groups = dict()
    current = data[0]['INN']
    groups[current] = []
    for e in data:
        if e['INN'] == current:
            groups[e['INN']].append({e['DATE']: e['EVENT']})
        else:
            current = e['INN']
            groups[current] = [{e['DATE']: e['EVENT']}]
    return groups


def is_actual(recommended_time, event_time):
    event_date = localtime(int(event_time) / 1000)
    rec_time = localtime(int(recommended_time) / 1000)

    rec_day = rec_time.tm_mday
    rec_month = rec_time.tm_mon
    rec_year = rec_time.tm_year

    event_day = event_date.tm_mday
    event_month = event_date.tm_mon
    event_year = event_date.tm_year

    if event_year > rec_year or event_month > rec_month or event_day > rec_day + 7:
        return False
    return True


def get_accuracy(groups):
    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0
    for key, values in groups.items():  # key - ИНН, values - список словарей (время: событие) каждого уникального
        if len(values) == 1:
            false_positive += 1  # пользователя
        else:
            r_time = 0
            for event in values:  # события пользователя
                if list(event.values())[0] == 'RECOMENDATION':
                    r_time = list(event.keys())[0]
                if list(event.values())[0] == 'PURCHASE' and r_time != 0:
                    if is_actual(list(event.keys())[0], list(event.keys())[0]):
                        true_positive += 1
                    else:
                        false_positive += 1
                        false_negative += 1
                if list(event.values())[0] == 'PURCHASE' and r_time == 0:
                    false_negative += 1
    print(true_positive, true_negative, false_positive, false_negative)
    return (true_negative + true_positive) / (true_negative + true_positive + false_negative + false_positive)


def get_metrics(data):
    data = get_actual_events(data)
    print(data)
    groups = create_groups(data)
    return get_accuracy(groups)
