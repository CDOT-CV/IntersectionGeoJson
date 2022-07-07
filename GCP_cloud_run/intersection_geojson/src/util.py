from dateutil.parser import parse
import pytz

# expects datetime
def format_date_utc(d):
  if(not d):
    return None
  tmp = parse(d)
  utc_tz = tmp.astimezone(pytz.UTC)
  return (utc_tz.strftime("%Y-%m-%dT%H:%M:%S"))

# expects datetime
def format_date_denver(d):
  if(not d):
    return None
  tmp = parse(d)
  denver_tz = tmp.astimezone(pytz.timezone('America/Denver'))
  return (denver_tz.strftime('%m/%d/%Y %I:%M:%S %p'))