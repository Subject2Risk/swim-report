#!/bin/python
from __future__ import print_function

def ppsd_event(data):
    if '25' in data['course']:
        course = 'S'
    else:
        course = 'L'
    return "({0}) {event:17}".format(course, **data)

def ppsd_time(row):
    return "{0}".format(row['time'].strftime("%M:%S.%f")[:-4])

def ppsd_date(row):
    return "{date:>12}".format(**row)

def ppsd_fina(row):
    return "{fina:4}".format(**row)

def ppsd_location(row):
    return "{location:>12}".format(**row)

def ppsd_meet(row):
    return "{meet}".format(**row)

def ppsd(row):
    return "{0} {1} {2} {3} {4} {5}".format(
                ppsd_event(row),
                ppsd_time(row),
                ppsd_date(row),
                ppsd_fina(row),
                ppsd_location(row),
                ppsd_meet(row))

def csv_field_convert(iterable, **conversion):
    for item in iterable:
        for key in item.viewkeys() & conversion:
            if item[key] is not None:
                item[key] = conversion[key](item[key])
        yield item

def str2time(val):
    from datetime import datetime
    def valset(val, index=None):
        if index is None:
            _x = val[-2:]
        else:
            _x = val[index - 2: index]
        if _x is None or len(_x) == 0:
            return '0'
        else:
            return _x

    val = val.replace(':','').replace('.','')

    f = valset(val)
    s = valset(val, -2)
    m = valset(val, -4)
    h = valset(val, -6)
    return datetime.strptime("{}:{}:{}.{}".format(h,m,s,f),"%H:%M:%S.%f")

def rlinput(prompt, prefill=''):
    import readline
    readline.set_startup_hook(lambda: readline.insert_text(prefill))
    try:
        return raw_input(prompt)
    finally:
        readline.set_startup_hook()

with open('5002181.csv') as f, open('temp.csv', 'wb') as out:
    import csv, sys
    columns = ['event', 'course', 'time', 'fina', 'date', 'location', 'meet', 'style', 'distance']
    reader = csv.DictReader(f, fieldnames=columns)
    reader = csv_field_convert(reader, **{'fina': int, 'distance': int, 'time': str2time })

    writer = csv.DictWriter(out, columns)

    for row in reader:
        while True:
            print("{:100}- Change (y/n)?".format(ppsd(row)), end='')
            if 'y' in str(raw_input()).lower().strip():
                prompt = "{} ".format(ppsd_event(row))
                thing = rlinput(prompt, "{}".format(ppsd_time(row)))
                row['time'] = str2time(thing)

                prompt = "{} {} ".format(ppsd_event(row), ppsd_time(row))
                row['date'] = rlinput(prompt, "{}".format(ppsd_date(row)))
                
                prompt = "{} {} {} ".format(ppsd_event(row), ppsd_time(row), ppsd_date(row))
                thing = rlinput(prompt, "{}".format(ppsd_fina(row)))
                row['fina'] = int(thing)

                prompt = "{} {} {} {} ".format(ppsd_event(row), ppsd_time(row), ppsd_date(row), ppsd_fina(row))
                row['location'] = rlinput(prompt, "{}".format(ppsd_location(row)))

                prompt = "{} {} {} {} {} ".format(ppsd_event(row), ppsd_time(row), ppsd_date(row), ppsd_fina(row), ppsd_location(row))
                row['meet'] = rlinput(prompt, "{}".format(ppsd_meet(row)))
            else:
                break

        row['time'] = ppsd_time(row)
        writer.writerow(row)
