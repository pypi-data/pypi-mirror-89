import isoweek

import logging
log = logging.getLogger("[🔧utilita]")
log.addHandler(logging.NullHandler()) # ignore log messages by defualt

def is_in_leap_week(date):
  return isoweek.Week.withdate(date).week == 53

def has_leap_week(year: int):
  return isoweek.Week(year, 53).week == 53

def last_year(date):
  return isoweek.Week.withdate(date).year - 1

def days_since_same_date_last_year(date):
  return 7 * 53 if is_in_leap_week(date) or has_leap_week(last_year(date)) else 7 * 52