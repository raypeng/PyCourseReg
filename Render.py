from Course import *
import random


colors = ['e1fed6', 'ffff66', 'ccff00', '66ffff', '00ccff', '66ff66',
          'ff99ff', '6699ff', 'cccccc', 'cc99ff', 'ffccff', '99cc99']
header = '''
<html>
 <head>
  <link href="timetable.css" rel="stylesheet" type="text/css"/>
  <td colspan="2" nowrap="nowrap">
   <table bgcolor="#ECE9D8" border="0" class="miniTimetable">
    <tr>
     <td bgcolor="#FFFFCC" nowrap="nowrap">
      <div class="timetable">
      </div>
     </td>
     <td bgcolor="#C6E2FF" height="5" nowrap="nowrap" width="90">
      <div class="timetable">
       Mon
      </div>
     </td>
     <td bgcolor="#C6E2FF" height="5" nowrap="nowrap" width="90">
      <div class="timetable">
       Tue
      </div>
     </td>
     <td bgcolor="#C6E2FF" height="5" nowrap="nowrap" width="90">
      <div class="timetable">
       Wed
      </div>
     </td>
     <td bgcolor="#C6E2FF" height="5" nowrap="nowrap" width="90">
      <div class="timetable">
       Thu
      </div>
     </td>
     <td bgcolor="#C6E2FF" height="5" nowrap="nowrap" width="90">
      <div class="timetable">
       Fri
      </div>
     </td>
    </tr>
'''
tail = '''
   </table>
  </td>
 </head>
</html>
'''


def random_colors(n):
    perm = range(len(colors))
    random.shuffle(perm)
    return [colors[perm[i]] for i in range(n)]


def convert(n):
    if n % 2 == 0:
        temp = '{0:02d}'.format(8 + n / 2)
	return '{0}:30 - {0}:50'.format(temp)
    else:
	temp = '{0:02d}'.format(9 + n / 2)
	return '{0}:00 - {0}:20'.format(temp)


def build_conversion():
    table = {}
    for i in range(1, 29):
        table[i] = convert(i)
    return table


def merge_map(time_map):
    keys = sorted(time_map.keys())
    for k in keys:
        if k not in time_map.keys():
            continue
        if k + 1 not in time_map.keys():
            continue
        i = 1
        while k + i in time_map.keys() and time_map[k] == time_map[k + i]:
            del time_map[k + i]
            i += 1
        time_map[k] = (time_map[k], i)
    return time_map


def convert_schedule(schedule, catalog):
    time_map = {}
    for course in schedule.keys():
        c = Course(catalog[course])
        sections = schedule[course][0].split()
        for s in sections:
            time = c.time[s]
            for t in time:
                time_map[t] = (course, s)
    occupied = time_map.keys()
    time_map = merge_map(time_map)
    return time_map, occupied


def time_entry(time, table):
    s = '<td bgcolor="#FFE3BB" height="5" nowrap="nowrap" width="90">' + \
        '<div class="timetable">{}</div></td>'.format(table[time])
    return s


def course_entry(time, time_map, color_map, occupied):
    s = ''
    if time in time_map.keys():
        course, section = time_map[time][0]
        rows = time_map[time][1]
        color = color_map[course]
        s = '<td align="center" bgcolor="#{}" height="5" '.format(color) + \
            'nowrap="nowrap" rowspan="{}" width="90">'.format(rows) + \
            '<div class="timetable"></div><div class="timetable">' + \
            '{0}<br/>{1}</div></td>'.format(course, section)
    elif time not in occupied:
        s = '<td bgcolor="#FFFFFF" height="5" nowrap="nowrap" width="90"></td>'
    return s        


def render_html(time_map, color_map, occupied):
    table = build_conversion()
    html = header
    for t in range(1, 29):
        html += '<tr>' + time_entry(t, table)
        for d in range(1, 6):
            time = 100 * d + t
            html += course_entry(time, time_map, color_map, occupied)
        html += '</tr>'
    html += tail
    return html


def save_html(schedule, catalog, path):
    count = len(schedule.keys())
    colors = random_colors(count)
    color_map = {course: colors.pop() for course in schedule.keys()}
    time_map, occupied = convert_schedule(schedule, catalog)
    html = render_html(time_map, color_map, occupied)
    with open(path, 'w') as f:
        f.write(html)
