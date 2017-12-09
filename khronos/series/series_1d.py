from __future__ import absolute_import

from ..utils.catch import catch_array, catch_split
from ..utils.time_utils import generate_timeline
from ..utils.visual import plot_ts

class series_1d:
    """Data structure for evenly spaced one dimentional time series
    
    Take an array as an input. Optionnaly take arguments to define the dates of
    the observations.
    
    The sampling dates can be supplied as a list (timeline)
    Alternatively, a first and last date of sampling can be given (with `start_date`
    and `end_date`), or a first date and a sampling periode (with `start_date` and `by`)
    If no optionnal argument are given, a start date of 0 and a periode of 1 is assumed
    
    # Arguments:
        values: Numpy Array, the values of the time serie.
        timeline: Array or list, the dates of observation of the values, must be
            the same length as `values`.
        start_date: A date object, the date of the first observation.
        end_date: A date object the date of the last observation.
        by: a time_delta, the periode between each sampling.
    """
    def __init__(self, values,
                 timeline=None,
                 start_date=None,
                 end_date=None,
                 by=None,
                 name=None):
        self.values = catch_array(values) #Test for array of length > 1
        self.N = len(values)
        self._splitted = False
        self.name = name
        
        if timeline is not None:
            #If a `timeline` was passed, we must sort the values in case `timeline` was not ordered
            if len(timeline)!=len(values): # Raise error if lengths are not consistent
                raise ValueError("Values and timeline should be of the same length")
            #Sort the values and unzip (convert to list to pass futur tests)
            a, b = zip(*sorted(zip(timeline, self.values)))
            self.timeline, self.values = list(a), catch_array(list(b))
        
        elif any(e is not None for e in (start_date, end_date, by)):
            self.timeline, _ = generate_timeline(self.N, start_date, end_date, by)
            
        else: #We must assume the default configuration
            self.timeline = range(self.N)
            
    def train_test_split(self, train=None, test=None, val=0):
        """Split the time serie into a training and a testing sets.
        
        #Arguments:
            train: float, the proportion of training points (default is 0.8)
            test: float, alternatively, the proportion of testing points
            val: float, proportion of validation points if we want such a validation set
        """
        if self._splitted: raise ValueError("The serie is already splitted")
        
        if train is None and test is None:
            train=0.8 # Assign a default value for train (0.8)
        train, test, val = catch_split(train, test, val)
        self._last_train_index = int(round(self.N * train))
        if val != 0:
            self._last_val_index = self._last_train_index + int(round(self.N * val))
        self._splitted = True
        
    def get_train(self):
        """Return the training part of the serie. Will fail if the serie is not splitted"""
        try:
            indx_train = self._last_train_index
        except:
            raise ValueError("Serie is not splitted. Call train_test_split to split it.")
        return series_1d(self.values[:indx_train],
                         self.timeline[:indx_train])
    
    def get_val(self,include_last=False):
        """Return the validation part of the serie. Will fail if the serie is not splitted
        #Arguments:
            include_last: bolean, if True, the last point of the training set is included"""
        try:
            indx_train = self._last_train_index
            indx_val = self._last_val_index
        except:
            raise ValueError("Serie is not splitted into a validation set. Call train_test_split to split it.")
        return series_1d(self.values[indx_train-include_last:indx_val],
                         self.timeline[indx_train-include_last:indx_val])
        
    def get_test(self,include_last=False):
        """Return the testing part of the serie. Will fail if the serie is not splitted
        #Arguments:
            include_last: bolean, if True, the last point of the previous set (train of val) is included"""
        try: # Does the serie has a validation set ?
            indx_val = self._last_val_index
            indx_train = self._last_train_index
        except:
            indx_val = False
            try: #If not, was it splitted ?
                indx_train = self._last_train_index
            except:
                raise ValueError("Serie is not splitted. Call train_test_split to split it.")
        if indx_val: #If a validation set was found, the test set start after it
            return series_1d(self.values[indx_val-include_last:],
                         self.timeline[indx_val-include_last:])
        else:
            return series_1d(self.values[indx_train-include_last:],
                         self.timeline[indx_train-include_last:])
            

    def plot(self,**kwargs):
        """Display the time serie (using pyplot)
        Just a call to the visualisation function from utils.visual
        """
        if 'style' not in kwargs.keys():
            style = 'classic'
        else:
            style = kwargs['style']
        plot_ts(self,style)
            
        
        
            
