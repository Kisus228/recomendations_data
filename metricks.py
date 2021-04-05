def create_groups(data):
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


def is_actual(rec_time, event_time):
    rec_day = int(rec_time.split()[0].split('.')[0])
    rec_month = int(rec_time.split()[0].split('.')[1])
    rec_year = int(rec_time.split()[0].split('.')[2])
    event_day = int(event_time.split()[0].split('.')[0])
    event_month = int(event_time.split()[0].split('.')[1])
    event_year = int(event_time.split()[0].split('.')[2])
    if event_year - rec_year > 0 or event_month - rec_month > 0 or event_day - rec_day > 2:
        return False
    return True


def getAccuracy(groups):
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


def getMetricks(data):
    groups = create_groups(data)
    return getAccuracy(groups)
