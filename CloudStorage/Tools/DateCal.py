#-*- coding: utf-8 -*-
from datetime import datetime, timedelta
import calendar


def prev_month_last_day(year, month):
    if month == 1:
        prev_month = 12
        prev_year = year - 1
    else:
        prev_month = month - 1
        prev_year = year
    days = calendar.monthrange(year, month)[1]
    result = datetime(prev_year, prev_month, 1) + timedelta(days=days)
    return result


def next_month_first_day(year, month):
    if month == 12:
        next_month = 1
        next_year = year + 1
    else:
        next_month = month + 1
        next_year = year
    return datetime(next_year, next_month, 1)