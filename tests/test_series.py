import pytest
import datetime
import numpy 
from khronos.series import series_1d
from khronos.series import generator
  
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

def test_split_1d():
    split_80 = series_1d(list(range(10)))
    split_80.train_test_split()
    assert list(split_80.get_train().values) == list(range(0,8))
    assert list(split_80.get_test(include_last=True).values) == list(range(7,10))
    assert list(split_80.get_test().values) ==list(range(8,10))
    with pytest.raises(ValueError):
        _ = split_80.get_val()
        
    split_30 =  series_1d(list(range(10)))
    split_30.train_test_split(test=0.3,val=0.3)
    assert list(split_30.get_train().values) == list(range(0,4))
    assert list(split_30.get_val().values) == list(range(4,7))
    assert list(split_30.get_val(include_last=True).values) == list(range(3,7))
    assert list(split_30.get_test().values) == list(range(7,10))
    
    split_50train = series_1d(list(range(10)))
    split_50test = series_1d(list(range(10)))
    split_50train.train_test_split(train = 0.4, val=0.2)
    split_50test.train_test_split(test = 0.4, val=0.2)
    assert split_50test._last_val_index == split_50train._last_val_index
    assert split_50test._last_train_index == split_50train._last_train_index
    
    with pytest.raises(ValueError):
        split_50train.train_test_split() #Try to split an already splitted serie
        
    with pytest.raises(ValueError):
        s = series_1d(list(range(10)))
        s.train_test_split(test=0.3,val=0.8)
    
    with pytest.raises(ValueError):
        s = series_1d(list(range(10)))
        s.train_test_split(train=0.3,val=0.8)
        
def test_generator():
    g1 = generator.gaussian_noise(10,scale=1)
    g1b = generator.gaussian_noise(10, start_date="01/01/2000", by="1d")
    l1 = generator.laplacian_noise(10,scale=1)
    l1b = generator.laplacian_noise(10, start_date="01/01/2000", by="1d")
    
    ARMAg1 = generator.ARMA_generator(10, p=[0.4,0.1], q=[0.4])
    ARMAg2 = generator.ARMA_generator(10, p=[0.4,0.1], q=[0.4], noise=numpy.random.normal(size=10))
    ARMAg2 = generator.ARMA_generator(10, p=[0.4,0.1], q=[0.4],
                                      noise=numpy.random.normal, noise_params={'scale':1})
    noise = numpy.zeros(6); noise[2] = 1
    ARMA3 = generator.ARMA_generator(6, p = [1,2], q=[0], noise=noise)
    assert list(ARMA3.values) == [0,0,1,1,3,5]
    ARMA4 = generator.ARMA_generator(6, p = [0], q=[0,1], noise=noise)
    assert list(ARMA4.values) == [0,0,1,0,1,0]
    
        
if __name__ == '__main__':
    pytest.main([__file__])
    