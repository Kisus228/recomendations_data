from collections import defaultdict

recommendation_period = 7
buffer = defaultdict(list)
days = []


def get_metrics(data: dict):
    update_actual_events(data)
    records = []
    for v in data.values():
        records += v
    groups = create_groups(records)
    return get_accuracy(groups)


# Заполняет буфер из recommendation_period дней
def update_actual_events(bd):
    days_event = list(bd.keys())
    events = list(bd.values())
    global buffer
    for i, val in enumerate(days_event):
        buffer[val].append(events[i])
    if len(days) > recommendation_period:
        day = days.pop(0)
        buffer.pop(day)


# возвращает группы действий по одному инн, т.е. несколько действий одного пользователя
def create_groups(data):
    groups = defaultdict(list)
    for e in data:
        groups[e['INN']].append(e['EVENT'])
    return groups


def get_accuracy(groups):
    global buffer, days
    true_positive, true_negative, false_positive, false_negative = 0, 0, 0, 0

    for key, values in groups.items():  # key - ИНН, values - список словарей (время: событие) каждого уникального
        for event in values:  # события пользователя
            if event == 'RECOMENDATION':
                false_positive += 1
            elif event == 'PURCHASE':
                if values[0] == 'RECOMENDATION':
                    true_positive += 1
                    false_positive -= 1
                else:
                    if is_recommended(key):
                        true_positive += 1
                    else:
                        false_negative += 1
    return (true_negative + true_positive) / (true_negative + true_positive + false_negative + false_positive)


def is_recommended(key):
    for k in buffer:
        for values in k:
            if values['INN'] == key and values['EVENT'] == 'RECOMENDATION':
                return True
    return False
