import os
import sys
import csv
import datetime


def str2date(str, date_format="%Y%m%d"):
    date = datetime.datetime.strptime(str, date_format)
    return date


def date2str(date, date_formate="%Y%m%d"):
    str = date.strftime(date_formate)
    return str


def save2csv():
    fileName = 'day_holiday_info' + '.csv'
    print('保存到csv文件(%s)中...' % (fileName,))
    with open(os.path.join(sys.path[0], fileName), 'w', encoding='utf-8-sig', newline='') as csvfile:
        fieldnames = ['day', 'weekday', 'isSatOrSun', 'isHoliday']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        start_date = str2date("20170101")
        end_date = str2date("20190519")
        while (end_date - start_date).days > 0:
            writer.writerow({'day': date2str(start_date), 'weekday': start_date.weekday(
            )+1, 'isSatOrSun': 'true' if start_date.weekday() >= 5 else 'false'})
            start_date = start_date + datetime.timedelta(days=1)

    print('保存完毕...')


if __name__ == '__main__':

    save2csv()
