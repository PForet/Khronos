import numpy 

def catch_length(x):
    """Return x if len(x) > 1, raise error else."""
    if len(x) < 2:
        raise ValueError("Array must contains at least two elements, got {}".format(x))
    return x

def catch_array(x):
    """Return x if x is list or array, else raise error """
    if isinstance(x,numpy.ndarray):
        return catch_length(x)
    elif isinstance(x,list):
        return numpy.array(catch_length(x))
    else:
        raise ValueError("Input must be a list or an array, got {}".format(x))
        
def catch_split(train=None, test=None, val=0):
    """Check if the train-test-(val) split is valid. Return the proportions if so."""
    
    if train is None and test is None: #Default values should be assigned before calling this function
        raise ValueError("train or test should be passed")
    if train is not None and (train > 1 or train < 0):
        raise ValueError("'train' should be a float between 0 and 1")
    if test is not None and (test > 1 or test < 0):
        raise ValueError("'test' should be a float between 0 and 1")
    if val > 1 or val < 0:
        raise ValueError("'val' should be a float between 0 and 1")
    
    if train is not None and test is not None:
        if train + test + val !=1:
            raise ValueError("All proportions should add up to one, got {}.".format(train+test+val))
    
    if train is not None and train+val > 1:
        raise ValueError("'train' plus 'val' already add up to more than one")
    
    if test is not None and test+val > 1:
        raise ValueError("'test' plus 'val' already add up to more than one")
    
    if train is None: #If 'test' is given, infer a correct value for 'train' instead of the default one
        train = 1 - test - val
    if test is None: 
        test = 1 - train - val
    
    return train, test, val