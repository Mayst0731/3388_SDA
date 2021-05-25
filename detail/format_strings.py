import re
from datetime import datetime
from dateutil.relativedelta import *

def get_tuition(price):
    tuition = ''
    tuition += ''.join(re.findall('\d+', price))
    if not tuition:
        tuition = int(tuition)
    return tuition


def get_currency(price):
    if 'S' or '$' or 'USD' in price:
        currency = 'USD'
    if '€' in price:
        currency = 'EUR'
    if "Lakh" in price:
        currency = 'LAC'
    return currency


def arrange_date_format(original_date):
    if len(original_date) == 0:
        return ''
    new_date = ''

    date_list = re.findall('\d{1,2}',original_date)
    if not date_list:
        date = '01'
    elif len(date_list) >= 1:
        date = date_list[0]
    if len(date) == 1:
        date = '0'+date

    month = month_dict(original_date)
    year_list = re.findall('\d{4}',original_date)
    if len(year_list) >= 1:
        year = year_list[0]
    else:
        year = original_date
    new_date = f'{year}-{month}-{date}'
    return new_date




def month_dict(month_str):
    months_check = {
            'Jan': '01',
            'Feb': '02',
            'Mar': '03',
            'Apr': '04',
            'May': '05',
            'Jun': '06',
            'Jul': '07',
            'Aug': '08',
            'Sep': '09',
            'Oct': '10',
            'Nov': '11',
            'Dec': '12',
        }
    for month in months_check.keys():
        if month in month_str:
            return months_check[month]


def get_duration_type(duration_info):
    type = ''
    if "Day" in duration_info:
        type = 'days'
    elif "Week" in duration_info:
        type = 'weeks'
    elif "year" in duration_info or "Year" in duration_info:
        type = 'years'
    elif "Month" in duration_info:
        type = 'months'
    return type


def get_duration_num(duration_info):
    if "One" in duration_info:
        num = 1
    else:
        num = re.findall('\d{1,2}',duration_info)[0]
        num = int(num)
    return num


def calculate_end_date(start_date,duration_type,duration_num):
    end_date = ''
    date = datetime.strptime(start_date, "%Y-%m-%d")
    if "months" in duration_type:
        mm = int(duration_num)
        end_date = date + relativedelta(months=+mm)
    elif "years" in duration_type:
        yy = int(duration_num)
        end_date = date + relativedelta(years=+yy)
    elif "weeks" in duration_type:
        ww = int(duration_num)
        end_date = date + relativedelta(weeks=+ww)
    if end_date != '':
        end_date = end_date.strftime("%Y-%m-%d")
    return end_date


def calculate_duration_info(start_date,end_date):

    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    difference = relativedelta(end_date,start_date)
    if difference.years:
        return {"duration_type": "months",
                "duration_num": difference.years*12}
    if difference.months:
        return {"duration_type": "months",
                "duration_num": difference.months}
    if difference.days:
        return {"duration_type": "days",
                "duration_num": difference.days}
    return {"duration_type": "",
                "duration_num": ""}










