#-*- coding: utf-8 -*-
from datetime import datetime
from dateutil import tz

mysql_timezone = None

def get_mysqltz():
    global mysql_timezone
    if mysql_timezone is None:
        from Models.Database import db
        from dateutil import tz
        result = db.engine.execute("SELECT TIMEDIFF(NOW(), UTC_TIMESTAMP) as result;").fetchall()[0][0]
        mysql_timezone=tz.tzoffset("mysql_time_zone",result.total_seconds())
    return mysql_timezone

def mysql_now():
    return datetime.utcnow().replace(tzinfo=tz.tzutc()).astimezone(get_mysqltz()).replace(tzinfo=None)

tzlocal_obj = tz.tzlocal()

def tzlocal_now():
    return datetime.now(tz=tzlocal_obj)