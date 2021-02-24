from bs4 import BeautifulSoup
import re
import requests
import json
import xlrd
import datetime


def get_schedule_from_mirea():
    page = requests.get('https://www.mirea.ru/schedule/')
    soup = BeautifulSoup(page.text, "html.parser")

    result = soup.find('div', {'class': 'rasspisanie'}).find(string='Институт информационных технологий').find_parent(
        'div').find_parent('div').findAll('a', {'class': 'uk-link-toggle'})
    for x in result:
        if re.search('ИИТ.*xlsx', str(x)):
            if re.search('1к', str(x)):
                f = open('file1.xlsx', 'wb')
                filexlsx = requests.get(x['href'])
                f.write(filexlsx.content)
                f.close()
            if re.search('2к', str(x)):
                f = open('file2.xlsx', 'wb')
                filexlsx = requests.get(x['href'])
                f.write(filexlsx.content)
                f.close()
            if re.search('3к', str(x)):
                f = open('file3.xlsx', 'wb')
                filexlsx = requests.get(x['href'])
                f.write(filexlsx.content)
                f.close()

    for n in range(1, 4):
        book = xlrd.open_workbook('file{}.xlsx'.format(n))
        sheet = book.sheet_by_index(0)

        num_cols = sheet.ncols
        num_rows = sheet.nrows

        groups_list = []
        groups = {}
        week_days = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']
        for col_index in range(num_cols):
            group_cell = str(sheet.cell(1, col_index).value)
            if re.search(r'\w{4}-\d\d-\d\d', group_cell):
                groups_list.append(group_cell)
                week = {'MON': None, 'TUE': None, 'WED': None, 'THU': None, 'FRI': None, 'SAT': None}
                for k in range(6):
                    day = [[], [], [], [], [], []]
                    for i in range(6):
                        for j in range(2):
                            subject = sheet.cell(3 + j + i * 2 + k * 12, col_index).value
                            lesson_type = sheet.cell(3 + j + i * 2 + k * 12, col_index + 1).value
                            lecturer = sheet.cell(3 + j + i * 2 + k * 12, col_index + 2).value
                            classroom = sheet.cell(3 + j + i * 2 + k * 12, col_index + 3).value
                            url = sheet.cell(3 + j + i * 2 + k * 12, col_index + 4).value
                            lesson = {'subject': subject, 'lesson_type': lesson_type, 'lecturer': lecturer,
                                      'classroom': classroom, 'url': url}
                            day[i].append(lesson)
                    week[week_days[k]] = day
                groups.update({group_cell: week})

        with open("groups{}.json".format(n), "w") as write_file:
            json.dump(groups, write_file)


def show_schedule_for_day(group, d):
    if d.weekday() == 6:
        return 'Занятий нет\n'
    course = -(int(group[-2::]) - 20)
    with open("groups{}.json".format(course), "r") as read_file:
        data = json.load(read_file)
    week_days = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']
    schedule = ''
    for i in range(6):
        str1 = str(i + 1) + ') '
        if data[group][week_days[d.weekday()]][i][(d.isocalendar()[1] + 1) % 2]['subject']:
            str1 += str(data[group][week_days[d.weekday()]][i][(d.isocalendar()[1] + 1) % 2]['subject']) + ', '
            if data[group][week_days[d.weekday()]][i][(d.isocalendar()[1] + 1) % 2]['lesson_type']:
                str1 += str(data[group][week_days[d.weekday()]][i][(d.isocalendar()[1] + 1) % 2]['lesson_type']) + ', '
            else:
                str1 += '--, '
            if data[group][week_days[d.weekday()]][i][(d.isocalendar()[1] + 1) % 2]['lecturer']:
                str1 += str(data[group][week_days[d.weekday()]][i][(d.isocalendar()[1] + 1) % 2]['lecturer']) + ', '
            else:
                str1 += '--, '
            if data[group][week_days[d.weekday()]][i][(d.isocalendar()[1] + 1) % 2]['classroom'] != 'Д':
                if data[group][week_days[d.weekday()]][i][(d.isocalendar()[1] + 1) % 2]['classroom']:
                    str1 += str(
                        data[group][week_days[d.weekday()]][i][(d.isocalendar()[1] + 1) % 2]['classroom']) + '\n'
                else:
                    str1 += '--\n'
            elif data[group][week_days[d.weekday()]][i][(d.isocalendar()[1] + 1) % 2]['url']:
                str1 += data[group][week_days[d.weekday()]][i][(d.isocalendar()[1] + 1) % 2]['url'] + '\n'
            else:
                str1 += '--\n'
        else:
            str1 += '--\n'
        schedule += str1
    return schedule


def show_schedule_for_week(group, d):
    d1 = d - datetime.timedelta(days=d.weekday())
    schedule = ''
    week_days = ['понедельник', 'вторник', 'среду', 'четверг', 'пятница', 'субботу']
    months = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября',
              'декабря']
    for i in range(6):
        schedule += 'Расписание на ' + week_days[i] + ' ' + str(d1.day) + ' ' + months[d1.month - 1] + ':\n'
        schedule += show_schedule_for_day(group, d1)
        d1 += datetime.timedelta(days=1)
    return schedule


def show_schedule_for_day_on_week(group, ind):
    schedule = ''
    week_days = ['понедельник', 'вторник', 'среду', 'четверг', 'пятница', 'субботу']
    schedule += 'Расписание на ' + week_days[ind] + ' чётной недели:\n' + show_schedule_for_day(group,
                                                                                                datetime.date(2020, 5,
                                                                                                              11) + datetime.timedelta(
                                                                                                    days=ind))
    schedule += 'Расписание на ' + week_days[ind] + ' нечётной недели:\n' + show_schedule_for_day(group,
                                                                                                  datetime.date(2020, 5,
                                                                                                                11) + datetime.timedelta(
                                                                                                      days=ind + 7))
    return schedule

get_schedule_from_mirea()
print(show_schedule_for_day_on_week('ИКБО-03-19',3))
