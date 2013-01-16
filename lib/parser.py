#-*- coding: UTF-8 -*-

from datetime import datetime, timedelta
import re
from const import DATE_SEP, TIME_SEP


class DateTimeParser():
    def __init__(self,text):
        self.now = self.__utc2loc(datetime.utcnow())
        self.text = text
        self.year = None
        self.month = None
        self.day = None
        self.hour = None
        self.minute = None
        self.second = None
        self.err_msg = ''
        self.target_datetime = None
        self.local_datetime = None
        self.remind_content = None

    def parser_text(self):
        tmp_text = self.text[::-1]
        p = re.compile(r'\bta\b|\bni\b',re.IGNORECASE)
        m = p.search(tmp_text)
        if m:
            self.remind_content = self.text[:0 - m.span()[1]].strip()
            time_field = self.text[0 - m.span()[0]:].strip()
            if m.group()[::-1].lower() == 'in':
                return self.parser_in(time_field)
            elif m.group()[::-1].lower() == 'at':
                return self.parser_at(time_field)
        else:
            self.err_msg = u'格式错误'
            return False
        return True

    def parser_in(self, time_field):
        time_field = re.compile('\s*').sub('', time_field)
        tmp_list = re.compile('\d+[a-zA-Z]').findall(time_field)

        time_dict = {}
        for item in tmp_list:
            t_key = re.compile('[a-zA-Z]').search(item).group()
            t_value = re.compile('\d+').search(item).group()
            time_dict[t_key] = t_value


        self.target_datetime = self.now
        for k, v in time_dict.iteritems():
            if k in ('d','D'):
                self.target_datetime += timedelta(days = int(v))
            elif k in ('h', 'H'):
                self.target_datetime += timedelta(hours = int(v))
            elif k in ('m', 'M'):
                self.target_datetime += timedelta(minutes = int(v))
            else:
                pass
        return self.gen_datetime(t_datetime = self.target_datetime)

    def parser_at(self, date_time_string):
        date_strings = []
        time_strings = []
        ap_string = []
        self.other_strings = []

        tmp_list = date_time_string.split()

        for item in tmp_list:
            if self.__char_in_string(item, DATE_SEP):
                date_strings.append(item)
            elif self.__char_in_string(item, TIME_SEP):
                time_strings.append(item)
            elif self.__char_in_string(item.lower(), ['am', 'pm', 'a', 'p']):
                ap_string.append(item)
            else:
                self.other_strings.append(item)

        self.other_strings = self.__filter_non_digit(self.other_strings)

        if not self.__parser_datetime_string(time_strings, t_type = 'time'):
            return False

        if not self.__parser_datetime_string(date_strings, t_type = 'date'):
            return False

        if self.other_strings:
            if self.year or self.month or self.day or self.hour or self.minute or self.second:
                return False
            else:
                if len(self.other_strings) != 1 or self.other_strings[0] > 60:
                    return False
                else:
                    self.minute = self.other_strings[0]

        return self.gen_datetime(ap_string = ap_string)

    def gen_datetime(self, t_datetime = None, ap_string = None):
        if not t_datetime:
            if not (self.year or self.month or self.day or self.hour or self.minute or self.second):
                self.err_msg = u'缺少有效的时间标志'
                return False

            if not (self.hour or self.minute):
                self.hour = 0
                self.minute = 0

            try:
                self.target_datetime = self.now.replace(year = self.year == None and self.now.year or self.year, month = self.month == None and self.now.month or self.month, day = self.day == None and self.now.day or self.day, hour = self.hour == None and self.now.hour or self.hour, minute = self.minute == None and self.now.minute or self.minute, second = 0)
            except Exception:
                self.err_msg = u'错误的时间格式'
                return False
        else:
            self.target_datetime = t_datetime

        if ap_string:
            if len(ap_string) > 1:
                self.err_msg = u'AM/PM 标志最多指定一个'
                return False
            if self.target_datetime.strftime('%p').lower() == 'am' and ap_string[0].lower() in ('p', 'pm'):
                self.target_datetime += timedelta(hours = 12)

        if self.target_datetime <= self.now:
            if not (self.year or self.month or self.day or self.hour or self.minute or self.second):
                self.err_msg = u'指定的时间须大于当前时间'
                return False
            elif self.hour == None:
                tmp_target = self.target_datetime + timedelta(hours = 1)
                if tmp_target <= self.now:
                    self.err_msg = u'指定的时间须大于当前时间'
                    return False
                else:
                    self.target_datetime = tmp_target
            elif not self.day:
                self.target_datetime += timedelta(days = 1)
            elif not self.month:
                new_month = self.target_datetime.month + 1
                new_year = self.target_datetime.year
                if new_month > 12:
                    new_year =+ 1
                    new_month -= 12
                self.target_datetime = self.target_datetime.replace(year = new_year, month = new_month)
            elif not self.year:
                new_year = self.target_datetime.year + 1
                self.target_datetime = self.target_datetime.replace(year = new_year)
            else:
                self.err_msg = u'指定的时间须大于当前时间'
                return False

        self.target_datetime = datetime.strptime('%s-%s-%s %s:%s' % (self.target_datetime.year, self.target_datetime.month, self.target_datetime.day, self.target_datetime.hour, self.target_datetime.minute), '%Y-%m-%d %H:%M')
        self.local_datetime = self.target_datetime
        self.target_datetime = self.__loc2utc(self.target_datetime)
        return True

    def __char_in_string(self, string, char_list):
        for char in char_list:
            if string.find(char) != -1:
                return True
        return False

    def __is_digit(self, s_list):
        p = re.compile('^\d+$')
        for item in s_list:
            if not p.search(item):
                return False
        return True

    def __filter_none_item(self, t_list):
        tmp_list = []
        for item in t_list:
            if item:
                tmp_list.append(item)
        return tmp_list

    def __filter_non_digit(self, t_list):
        p = re.compile('^\d+$')
        tmp_list = []
        for item in t_list:
            if p.search(item):
                tmp_list.append(int(item))
        return tmp_list

    def __parser_datetime_string(self, strings, t_type):
        if not strings:
            return True
        elif len(strings) >1:
            self.err_msg = u'含有多余时间字段'
            return False
        else:
            if t_type == 'time':
                sep = TIME_SEP
            else:
                sep = DATE_SEP
            p = re.compile('|'.join(sep).replace('.', '\.'))
            t_list = p.split(strings[0])
            t_list = self.__filter_none_item(t_list)

            if not t_list:
                self.err_msg = u'含有非法字段'
                return False
            elif len(t_list) > 3:
                self.err_msg = u'含有多余的字段'
                return False
            elif not self.__is_digit(t_list):
                self.err_msg = u'含有非法字符'
                return False
            else:
                for i in range(len(t_list)):
                    t_list[i] = int(t_list[i])

                if t_type == 'time':
                    return self.__parser_time_list(t_list)
                else:
                    return self.__parser_date_list(t_list)
        return True

    def __parser_time_list(self,t_list):
        if len(t_list) == 1:
            self.minute = t_list[0]
            if self.minute > 60:
                self.err_msg = u'时间格式错误'
                return False
        else:
            self.hour = t_list[0]
            self.minute = t_list[1]

        if self.hour > 24 or self.minute > 60:
            if self.hour <= 60 and self.minute <= 24 and len(t_list) == 2:
                (self.hour, self.minute) = (self.minute, self.hour)
            else:
                self.err_msg = u'时间格式错误'
                return False
        return True

    def __parser_date_list(self, date_list):
        if len(date_list) == 1:
            self.day = date_list[0]
        elif len(date_list) == 2:
            self.month = date_list[0]
            self.day = date_list[1]
        elif len(date_list) == 3:
            if date_list[2] <= 31:
                self.year = date_list[0]
                self.month = date_list[1]
                self.day = date_list[2]
            else:
                self.month = date_list[0]
                self.day = date_list[1]
                self.year = date_list[2]
        return True

    def __parser_ap_string(self, time_string):
        if time_string:
            if self.__char_in_string(time_string[0].lower(), ['p', 'pm']):
                pass

    def __loc2utc(self, local_date):
        utc_date = local_date - timedelta(hours=+8)
        return utc_date

    def __utc2loc(self,utc_date):
        loc_date = utc_date + timedelta(hours=+8)
        return loc_date
