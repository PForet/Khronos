import pytest
from khronos.utils import time_utils as tu

def test_generate_timeline():
    #Three methods of generation with the same delta time
    tl1, dt1 = tu.generate_timeline(10,start_date="01/01/1000",by="1d")
    tl2, dt2 = tu.generate_timeline(2,start_date="01/01/2000",end_date="02/01/2000")
    tl3, dt3 = tu.generate_timeline(100,end_date="01/01/2000",by="1d")
    
    assert dt1 == dt2
    assert dt1 == dt3
    
    tl4, dt4 = tu.generate_timeline(31416, start_date="01/01/1000", by="2d")
    assert dt1 != dt4
    
    with pytest.raises(ValueError): #Not enought arguments
        tl5 = tu.generate_timeline(10,start_date="01/01/2000")

def test_delta_to_years():
    day1 = tu.coerce_timedelta("1d")
    assert tu.delta_to_years(day1) == 1/365.25
    
    one_small_month = tu.coerce_timedelta("28d")
    one_large_month = tu.coerce_timedelta("31d")
    one_month = tu.coerce_timedelta("1m")
    # All is independant from today's date, but quicker to test like this
    assert one_month > one_small_month and one_month < one_large_month
    assert tu.delta_to_years(one_month) > tu.delta_to_years(one_small_month)
    assert tu.delta_to_years(one_month) < tu.delta_to_years(one_large_month)
    
    assert abs(tu.delta_to_years(tu.coerce_timedelta("1d"))*365.25 - tu.delta_to_years(tu.coerce_timedelta("1y"))) < 10e-4
    
    