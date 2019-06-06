import pytz


def localTime(date):
    tz = pytz.timezone('Africa/Nairobi')
    utc = pytz.timezone('UTC')
    tz_aware_dt = utc.localize(date)
    local_dt = tz_aware_dt.astimezone(tz)
    return local_dt.strftime("%H:%M:%S")