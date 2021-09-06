import datetime


def respprint(obj):
    if type(obj) == str:
        print(obj)
    else:
        keys = list(obj[0].keys())
        print('------------'*12)
        for item in keys:
            print("{0:18s}".format(item), end='')
        print()
        print('------------'*12)
        for item in obj:
            for element in item:
                print("{0:18s}".format(str(item[element])), end='')
            print()
        print('------------'*12)
