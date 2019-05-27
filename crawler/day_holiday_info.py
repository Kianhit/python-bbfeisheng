import os
import sys
import csv
import datetime
import time
import argparse
from collections import ChainMap
import sxtwl


class DayInfoPrep(object):
    def __init__(self, start_date, end_date):
        self._start_date = self.str2date(start_date)
        self._end_date = self.str2date(end_date)
        self._holiday_not_work = [
            20170101, 20170102,
            20170127, 20170128, 20170129, 20170130, 20170131, 20170101, 20170102,
            20170402, 20170403, 20170404,
            20170429, 20170430, 20170501,
            20170528, 20170529, 20170530,
            20171001, 20171002, 20171003, 20171004, 20171005, 20171006, 20171007, 20171008,
            20171230, 20171231,
            20180101,
            20180215, 20180216, 20180217, 20180218, 20180219, 20180220, 20180221,
            20180405, 20180406, 20180407,
            20180429, 20180430, 20180501,
            20180616, 20180617, 20180618,
            20180922, 20180923, 20180924,
            20181001, 20181002, 20181003, 20181004, 20181005, 20181006, 20181007,
            20181230, 20181231,
            20190101,
            20190204, 20190205, 20190206, 20190207, 20190208, 20190209, 20190210,
            20190405, 20190404, 20190407,
            20190501, 20190502, 20190503, 20190504,
            20190607, 20190608, 20190609,
            20170211,
            20190113,
            20170514,
            20170618,
            20180617,
            20180513,
            20170514,
            20170618,
            20190616,
            20190512,
            20191007,
            20171028,
            20171224,
            20170520,
            20180520]
        self._holiday_work = [
            20170214,
            20180214,
            20190214,
            20180302,
            20190219,
            20180124,
            20181122,
            20171123,
            20170308,
            20180308,
            20190308,
            20180601,
            20170601,
            20170828,
            20180817,
            20190807,
            20181017,
            20171225,
            20181225,
            20181224,
            20190520]
        self._weekend_work = [
            20170101,
            20170122, 20170204,
            20170401,
            20170527,
            20170930,
            20180211, 20180224,
            20180408,
            20180428,
            20180929, 20180930,
            20181229,
            20190202, 20190203,
            20190428, 20190505,
            20190601
        ]
        self._ymc = [u"十一", u"十二", u"正", u"二", u"三",
                     u"四", u"五", u"六", u"七", u"八", u"九", u"十"]
        self._ymc_num = [u"11", u"12", u"01", u"02", u"03",
                         u"04", u"05", u"06", u"07", u"08", u"09", u"10"]
        self._rmc = [u"初一", u"初二", u"初三", u"初四", u"初五", u"初六", u"初七", u"初八", u"初九", u"初十",
                     u"十一", u"十二", u"十三", u"十四", u"十五", u"十六", u"十七", u"十八", u"十九",
                     u"二十", u"廿一", u"廿二", u"廿三", u"廿四", u"廿五", u"廿六", u"廿七", u"廿八", u"廿九", u"三十", u"卅一"]
        self._rmc_num = [u"01", u"02", u"03", u"04", u"05", u"06", u"07", u"08", u"09", u"10",
                         u"11", u"12", u"13", u"14", u"15", u"16", u"17", u"18", u"19",
                         u"20", u"21", u"22", u"23", u"24", u"25", u"26", u"27", u"28", u"29", u"30", u"31"]

    def str2date(self, str, date_format="%Y%m%d"):
        date = datetime.datetime.strptime(str, date_format)
        return date

    def date2str(self, date, date_formate="%Y%m%d"):
        str = date.strftime(date_formate)
        return str

    def date_delta(self, date, gap, formate="%Y%m%d"):
        date = self.str2date(date)
        pre_date = date + datetime.timedelta(days=-gap)
        pre_str = self.date2str(pre_date, formate)  # date形式转化为str
        return pre_str

    def str2timestamp(self, str, timestamp_len=10):
        date_array = time.strptime(str, "%Y-%m-%d %H:%M:%S")
        timestamp = int(time.mktime(date_array))
        if timestamp_len == 13:
            timestamp *= 1000
        return timestamp

    def get_week_day(self, date):
        week_day_dict = {
            0: '星期一',
            1: '星期二',
            2: '星期三',
            3: '星期四',
            4: '星期五',
            5: '星期六',
            6: '星期天',
        }
        return week_day_dict[date.weekday()]

    def save2csv(self):
        lunar = sxtwl.Lunar()  # 实例化日历库
        fileName = 'day_holiday_info' + '.csv'
        print('保存到csv文件(%s)中...' % (fileName,))
        with open(os.path.join(sys.path[0], fileName), 'w', encoding='utf-8-sig', newline='') as csvfile:
            fieldnames = ['day', 'lunar_day_name', 'lunar_day',
                          'week_day', 'week_day_name', 'day_type', 'day_type_id']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            start_date = self._start_date
            while (self._end_date - start_date).days > 0:
                day_str = self.date2str(start_date)
                start_date_num = int(day_str)
                day = lunar.getDayBySolar(
                    int(day_str[0:4]), int(day_str[4:6]), int(day_str[6:]))

                if start_date_num in self._holiday_not_work:
                    day_type = '节假日'
                    day_type_id = '1'
                elif start_date_num in self._holiday_work:
                    day_type = '工作日(节日)'
                    day_type_id = '4'
                elif start_date.weekday() >= 5 and start_date_num not in self._weekend_work:
                    day_type = '双休日'
                    day_type_id = '3'
                else:
                    day_type = '工作日'
                    day_type_id = '2'

                writer.writerow({
                    'day': start_date_num,
                    'lunar_day_name': self._ymc[day.Lmc] + u"月" + self._rmc[day.Ldi] + ("" if '初' in self._rmc[day.Ldi] else u"日"),
                    'lunar_day': self._ymc_num[day.Lmc] + self._rmc_num[day.Ldi],
                    'week_day': start_date.weekday()+1,
                    'week_day_name': self.get_week_day(start_date),
                    'day_type': day_type,
                    'day_type_id': day_type_id})
                start_date = start_date + datetime.timedelta(days=1)

        print('保存完毕...')


if __name__ == '__main__':

    defaults = {'start': '20170101', 'end': '20190519'}
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--start')
    parser.add_argument('-e', '--end')
    namespace = parser.parse_args()
    command_line_args = {k: v for k, v in vars(namespace).items() if v}
    combined = ChainMap(command_line_args, defaults)
    DayInfoPrep(combined['start'], combined['end']).save2csv()
