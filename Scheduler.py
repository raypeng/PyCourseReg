from Course import *
from Parser import *
from Render import *
import datetime
import os


def write_css(path):
    css = '''
    .timetable {
      font-family:"Arial";
      font-size: 8.5pt;
      text-align: center;
    }
    '''
    with open(path, 'w') as f:
        f.write(css)

        
def is_valid(time_list):
    return len(time_list) == len(set(time_list))


def get_solution(schedule_list):
    ans = ''
    for i in range(len(schedule_list)):
        schedule = schedule_list[i]
        ans += 'Solution #' + str(i + 1) + '\n'
        sol = '\n'.join(course + ' ' + schedule[course][0]
                        for course in schedule)
        ans += sol + '\n'
    return ans

        
INDEX = 'https://w5.ab.ust.hk/wcq/cgi-bin/1410/'
JSON_FILE = 'courses.json'
FOLDER = 'PyCourseReg'
print '============ WELCOME TO PyCourseReg v0.1 ============'

try:
    path = os.path.join(JSON_FILE)
    catalog = load_json(path)
    print 'Course info loaded from local disk...'
except:
    print 'Grabbing course info from the web...'
    catalog = parse_url(INDEX)
    print 'Course info parsing done...'
    save_json(catalog, JSON_FILE)
    print 'Course info saved to local disk...'
    
options = {}
for k, v in catalog.iteritems():
    t = Course(v)
    options[k] = t.options

if os.path.exists(FOLDER):
    pass
else:
    os.mkdir(FOLDER)

wish_list = []
schedule_list = []
print
while True:
    ans = raw_input('Enter a course code(sample: UROP 1400H) \n' + \
                    'or "s" to save schedules or "e" to end: ')
    if ans == 's':
        write_css(os.path.join(FOLDER, 'timetable.css'))
        time = str(datetime.datetime.now())
        timestamp = time[5:7] + time[8:10] + time[11:13] + time[14:16]
        file_name = 'schedules_' + timestamp + '.txt'        
        path = os.path.join(FOLDER, file_name)
        with open(path, 'w') as f:
            f.write(get_solution(schedule_list))
        print 'Schedule summary saved to "{}"!'.format(path)
        for s in schedule_list:
            file_name = 'sol_' + timestamp + '_' + \
                        str(schedule_list.index(s) + 1) + '.html'
            path = os.path.join(FOLDER, file_name)
            save_html(s, catalog, path)
        print 'Schedule timetables saved, see .html files.'
        print
        continue
    if ans == 'e':
        print 'Thanks for using! Bye!'
        break
    if ans not in options.keys():
        print 'Invalid Course! Try Again!'
        continue
    if ans in wish_list:
        print 'Already have that! Pick a new one!'
        continue
    if not options[ans]:
        print 'That is a not-on-schedule course! Come on! Another one!'
        continue
    
    wish_list.append(ans)
    schedule_list = []
    schedule = {}
    count = len(wish_list)
    prod = [options[course].keys() for course in wish_list]
    for perm in product(*prod): 
        temp = dict(schedule)
        time = reduce(lambda x, y: x + y, \
                      [options[wish_list[i]][perm[i]] for i in range(count)])
        if is_valid(time):
            for i in range(count):
                temp[wish_list[i]] = (perm[i], options[wish_list[i]][perm[i]])
            schedule_list.append(temp)
    if len(schedule_list) == 0:
        print 'Sorry, time conflicts! Consider another one other than ' + ans
        print
        wish_list.remove(ans)
        continue
    
    print 'Wish List: ' + ', '.join(s for s in wish_list)
    print 'Returning ' + str(len(schedule_list)) + ' schedules.'
    print
    ans = raw_input('Wanna see the details? (y/n) ')
    if ans.lower() == 'y':
        print get_solution(schedule_list)
