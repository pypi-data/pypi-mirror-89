import isoweek

import logging
log = logging.getLogger("[🔧utilita]")
log.addHandler(logging.NullHandler()) # ignore log messages by defualt

def is_in_leap_week(date):
  return isoweek.Week.withdate(date).week == 53

def days_since_same_date_last_year(date):
  return 7 * 52 if not is_in_leap_week(date) else 7 * 53