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


def getAccuracy(groups):
    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0
    for key in groups:
        print(groups[key])  # for event in groups[key]:
        #   print(event.values())


def getMetricks(data):
    groups = create_groups(data)
    getAccuracy(groups)
