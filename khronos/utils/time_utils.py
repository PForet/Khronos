import datetime

def coerce_date(d):
    """Try to convert `d` to a datetime objects. The available formats are:
        - "dd-mm-yyyy"
        - "dd/mm/yyyy"
        - "yyyy/mm/dd"
        - "yyy-mm-dd"
    Raise an error if the parsing fails.
    """
    parsed_date = None
    formats = ("%Y-%m-%d","%Y/%m/%d","%d-%m-%Y","%d/%m/%Y")
    for f in formats:
        try:
            parsed_date = datetime.datetime.strptime(d,f)
        except:
            pass
    if parsed_date is None:
        raise ValueError("Failed to parse date: {}".format(d))
    return parsed_date

def coerce_timedelta(d):
    """Try to convert `d` into a timedelta object. The available formats are:
        - '[n]d' for n days
        - '[n]m' for n months
        - '[n]y' for n years
    Example: '2d' is two days, '0.5y' is six months.
    """
    try:
        if d[-1] == 'd':
            return datetime.timedelta(days=float(d[:-1]))
        if d[-1] == 'm':
            return datetime.timedelta(days=30.4*float(d[:-1]))
        if d[-1] == 'y':
            return datetime.timedelta(days=365*float(d[:-1]))
    except:
        raise ValueError("Failed to parse period: {}".format(d))
    
def evenly_spaced_timeline(start_date, end_date, size):
    """Return a list of `size` datetime objects evenly spaced between `start_date` and `end_date`."""
    if not isinstance(start_date, datetime.datetime):
        start_date = coerce_date(start_date)
    if not isinstance(end_date, datetime.datetime):
        end_date = coerce_date(end_date)
    if end_date < start_date: 
        raise ValueError("end_date is before start_date")
    _delta = (end_date-start_date)/(size-1)
    return([start_date + i*_delta for i in range(size)])

def fixed_period_timeline(ref_date, period, size):
    """Return a list of `size` datetime objects evenly spaced by `period`.
    `period` should be a timedelta or a coercible string (1d, 1m, 1y).
    If `period` is negative, the `ref_date` is considerated the last date of the list.
    If `period` is positive, the `ref_date` is considerated the fist date of the list.
    
    """
    if not isinstance(ref_date, datetime.datetime):
        ref_date = coerce_date(ref_date)
    if not isinstance(period, datetime.timedelta):
        period = coerce_timedelta(period)
    lst_date = [ref_date + i*period for i in range(size)]
    if period < datetime.timedelta(days=0): #if ref date is the last date
        return lst_date[::-1] #invert list
    else:
        return lst_date
    
def delta_to_years(tdelta):
    """Approximate à timedelta object by a float representing the number of years"""
    return tdelta.total_seconds()/3600.0/24.0/365.25

def generate_timeline(N, start_date=None, end_date=None, by=None):
    """Generate a datetime objects list (timeline) according to the arguments.
    A first and last date of sampling can be given (with `start_date`
    and `end_date`), or a first or last date and a sampling periode (with `start_date` and `by`)
    
    # Arguments:
        values: Numpy Array, the values of the time serie.
        timeline: Array or list, the dates of observation of the values, must be
            the same length as `values`.
        start_date: A date object, the date of the first observation.
        end_date: A date object the date of the last observation.
        by: a time_delta, the periode between each sampling.
    
    Return a timeline and and the sampling period (float, number of years)
    """
    if start_date is not None and by is not None:
        timeline = fixed_period_timeline(start_date, by, N)
    elif end_date is not None and by is not None:
        # If we pass the last date, we need to put a minus before by (string of number)
        timeline = fixed_period_timeline(end_date,("-"+by if isinstance(by,str) else -by), N)
    elif start_date is not None and end_date is not None:
        timeline = evenly_spaced_timeline(start_date, end_date, N)
    else:
        raise ValueError("Should provide two of the following: 'start_date', 'end_date', 'by'")
    delta_t = delta_to_years(timeline[1] - timeline[0])
    return timeline, delta_t

