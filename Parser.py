# -*- coding: utf-8 -*-
import urllib2
import json
import re


def replace_dict(s, d):
    for key, val in d.iteritems():
        s = s.replace(key, str(val))
    return s

    
def map_time(s):
    ''' input ~ 'TuTh 09:00AM - 10:20AM'
    '''
    day_map = {'Mo': 1, 'Tu': 2, 'We': 3, 'Th': 4, 'Fr': 5, 'Sa': 6, 'Su': 7}
    time_replace = {'12:20': '12:30', '12:50': '01:00',
                    '01:20': '01:30', '01:50': '02:00',
                    '02:20': '02:30', '02:50': '03:00',
                    '03:20': '03:30', '03:50': '04:00',
                    '04:20': '04:30', '04:50': '05:00',
                    '05:20': '05:30', '05:50': '06:00',
                    '06:20': '06:30', '06:50': '07:00',
                    '07:20': '07:30', '07:50': '08:00',
                    '08:20': '08:30', '08:50': '09:00',
                    '09:20': '09:30', '09:50': '10:00',
                    '10:20': '10:30', '10:50': '11:00',
                    '11:20': '11:30', '11:50AM': '12:00PM'}
    time_map = {'09:00AM': 1,  '09:30AM': 2,  '10:00AM': 3,  '10:30AM': 4, 
                '11:00AM': 5,  '11:30AM': 6,  '12:00PM': 7,  '12:30PM': 8, 
                '01:00PM': 9,  '01:30PM': 10, '02:00PM': 11, '02:30PM': 12,
                '03:00PM': 13, '03:30PM': 14, '04:00PM': 15, '04:30PM': 16, 
                '05:00PM': 17, '05:30PM': 18, '06:00PM': 19, '06:30PM': 20, 
                '07:00PM': 21, '07:30PM': 22, '08:00PM': 23, '08:30PM': 24,
                '09:00PM': 25, '09:30PM': 26, '10:00PM': 27, '10:30PM': 28,
                '11:00PM': 29, '11:30PM': 30}
    day, time = tuple(s.split(' ', 1))
    day_list = [int(char) for char in replace_dict(day, day_map)]
    time_str = replace_dict(replace_dict(time, time_replace), time_map)
    lower, upper = tuple(map(int, time_str.split(' - ')))
    time = [map(lambda x: x + 100 * d, range(lower, upper)) for d in day_list]
    return [tt for t in time for tt in t]

    
def parse_datetime(str_list):
    ''' input ~ ['L1 (3091)</td>\n<td>TuTh 09:00AM - 10:20AM',
                 'T1A (3093)</td>\n<td>Th 06:00PM - 06:50PM',
                 'T1B (3095)</td>\n<td>Fr 06:00PM - 06:50PM']
        output ~ {'tut': {}, 'lab': {'1': [406, 407, 408, 409]}, 
                 'credit': 4.0, 'lec': {'1': [216, 217, 218, 416,
                 417, 418]}}
    '''
    lec, tut, lab = {}, {}, {}
    for s in str_list:
        if '<br>' in s:
            time_raw = re.search(r'(?<=<br>).*', s).group()
        else:            
            time_raw = re.search(r'(?<=<td>).*', s).group()
        if time_raw == 'TBA':
            continue
        time = map_time(time_raw)
        name_raw = re.match(r'.*?(?= )', s).group()
        if 'R' in name_raw:
            continue
        elif 'LA' in name_raw:
            session = name_raw[2:]
            lab[session] = time
        elif 'T' in name_raw:
            session = name_raw[1:]
            tut[session] = time
        else:
            session = name_raw[1:]
            lec[session] = time
    return {'lec': lec, 'tut': tut, 'lab': lab}
           

def parse_str(s):
    ''' output ~ {'code': 'PHYS 1112', 'title': 'General Physics I 
                   with Calculus', 'tut': {'2D': [302, 303], '1A': 
                   [211, 212], '1C': [214, 215], '1B': [211, 212], 
                   '1D': [214, 215], '2B': [508, 509], '2C': [302, 
                   303], '3C': [311, 312], '3B': [219, 220], '3A': 
                   [219, 220], '3D': [311, 312], '2A': [508, 509]}, 
                   'lab': {}, 'credit': 3.0, 'lec': {'1': [201, 202,
                   203, 401, 402, 403], '3': [316, 317, 318, 516, 
                   517, 518], '2': [310, 311, 312, 510, 511, 512]}, 
                   'matching': True}
    '''
    intro = re.search(r'(?<=<h2>)(?P<code>.*?) - (?P<title>.*) ' \
               + r'\((?P<credits>[\d+.]*\d+) unit[s]*\)(?=</h2>)', s)
    info = intro.groupdict()
    info['credits'] = float(info['credits'])
    if '<div class="matching">' in s:
        info['matching'] = True
    else:
        info['matching'] = False
    temp = re.findall(r'(?<=">).*</td>\n<td>.*?(?=</td>)', s)
    datetime = parse_datetime(temp)
    return dict(info.items() + datetime.items())
    

def parse_url(INDEX_URL):
    response = urllib2.urlopen(INDEX_URL)
    html = response.read()
    depts_match = re.search(r'(?<=<div class="depts">).*(?=</div>)', html)
    depts = re.findall(r'(?<=">)\w{4}(?=</a>)', depts_match.group())
    catalog = {}
    for dept in depts:
        dept_url = INDEX_URL + 'subject/' + dept
        response = urllib2.urlopen(dept_url)
        html = response.read()
        data = html.split('<script type="text/javascript">')
        data = data[1]
        courses = data.split('<div class="course">')
        courses = courses[1:]
        for course in courses:
            info = parse_str(course)
            catalog[info['code']] = info
    return catalog


def save_json(catalog, outfile):
    with open(outfile, 'w') as f:
        json.dump(catalog, f, encoding='utf-8')


def load_json(infile):
    with open(infile, 'r') as f:
        return json.load(f, encoding='utf-8')
