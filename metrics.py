from collections import defaultdict

recommendation_period = 7
buffer = []
days = []


# Заполняет буфер из recommendation_period дней
def update_actual_events(events):
    global buffer
    if len(buffer) > recommendation_period:
        buffer.pop(0)
        buffer.append(events)
    else:
        buffer.append(events)


# возвращает группы действий по одному инн, т.е. несколько действий одного пользователя
def create_groups(data):
    groups = defaultdict(list)
    for e in data:
        groups[e['INN']].append(e['EVENT'])
    return groups, data[0]['DATE_DD_MM_YYYY']


def is_recommended(key):
    for k in buffer:
        for values in k:
            if values['INN'] == key and values['EVENT'] == 'RECOMENDATION':
                return True
    return False


def get_accuracy(groups, day):
    global buffer, days
    true_positive, true_negative, false_positive, false_negative = 0, 0, 0, 0
    update_global_variable(day)

    for key, values in groups.items():  # key - ИНН, values - список словарей (время: событие) каждого уникального
        for event in values:  # события пользователя
            if event == 'RECOMENDATION':
                false_positive += 1
            elif event == 'PURCHASE':
                if values[0] == 'RECOMENDATION':
                    true_positive += 1
                    false_positive -= 1
                else:
                    day_update = is_recommended(key)
                    if day_update is not None:
                        true_positive += 1
                    else:
                        false_negative += 1
    return (true_negative + true_positive) / (true_negative + true_positive + false_negative + false_positive)


def update_global_variable(day):
    days.append(day)
    if len(days) > recommendation_period:
        days.pop(0)


def get_metrics(data):
    update_actual_events(data)
    groups, day = create_groups(data)
    return get_accuracy(groups, day)
