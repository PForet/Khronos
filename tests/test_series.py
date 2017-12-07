import pytest
import datetime
from khronos.series import series_1d
  
def test_series_1d():
    # Test several ways of defining a serie
    s = series_1d([1,2,3,4,5], start_date='01-01-2000',by='0.5y')
    assert all(isinstance(e,datetime.datetime) for e in s.timeline)
    s = series_1d([1,2,3,4,5], end_date='01/01/2010', by='12.35m')
    assert all(isinstance(e,datetime.datetime) for e in s.timeline)
    s = series_1d([1,2,3,4,5], start_date='01/01/2000', end_date='01/01/2012')
    assert all(isinstance(e,datetime.datetime) for e in s.timeline)
    # Test if the serie is sorted according to timeline
    s1 = series_1d([1,2,3,4,5])
    s1_bis = series_1d([1,2,5,4,3], timeline=[10,20,100,50,30])
    assert list(s1.values) == list(s1_bis.values)
    # Test for exeption if the inputs are not legal
    with pytest.raises(ValueError):
        s = series_1d([2]) #Should fail as only one value is passed
    with pytest.raises(ValueError):
        #Should fail as timeline and values are different length
        s = series_1d([1,2], timeline=[1,2,3])
    with pytest.raises(ValueError):
        #Should fail as end_date is after start_date
        s = series_1d([1,2], start_date='01/01/2012', end_date='01/01/2000')
    with pytest.raises(ValueError):
        #Should fail as a start_date alone is not sufficient
        s = series_1d([1,2,3], start_date='01/01/2012')

        
if __name__ == '__main__':
    pytest.main([__file__])
    