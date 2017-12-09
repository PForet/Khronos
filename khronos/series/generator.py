from ..series import series_1d
from ..utils.time_utils import generate_timeline
import numpy

def gaussian_noise(size, scale=1, **kwargs):
    """Generate a gaussian noise (independant gaussian vector) of a given size, as a series_1d object
    
    # Arguments:
        size: int, the size of the time serie to generate
        scale: the standard deviation of the gaussian noise (yearly if a dated timeline is used)
        kwargs: arguments to generate a dated timeline (see series_1d arguments)
    """
    if any(e in kwargs.keys() for e in ('start_date', 'by', 'end_date')):
        # A dated timeline will be generated
        timeline, delta_t = generate_timeline(size, **kwargs)
    else:
        timeline, delta_t = range(size), 1 # 1 sample each unit of time by default
    # Need to recale the yearly standard deviation
    values = _noise_generator('gaussian', size=size, param_dict={'scale':scale*numpy.sqrt(delta_t)})
    return series_1d(values, timeline, name="Gaussian noise (scale={})".format(scale))

def laplacian_noise(size, scale=1, **kwargs):
    """Generate a laplacian noise (difference between two exponential variables) of a given size, as a series_1d object
    
    # Arguments:
        size: int, the size of the time serie to generate
        scale: the standard deviation of the gaussian noise (yearly if a dated timeline is used)
        kwargs: arguments to generate a dated timeline (see series_1d arguments)
    """
    if any(e in kwargs.keys() for e in ('start_date', 'by', 'end_date')):
        # A dated timeline will be generated
        timeline, delta_t = generate_timeline(size, **kwargs)
    else:
        timeline, delta_t = range(size), 1 # 1 sample each unit of time by default
    # Need to recale the yearly standard deviation
    values = _noise_generator('laplace', size=size, param_dict={'scale':scale*numpy.sqrt(delta_t)})
    return series_1d(values, timeline, name="Laplacian noise (scale={})".format(scale))

def ARMA_generator(size, p, q, noise='gaussian', noise_params={}, **kwargs):
    """Generate an ARMA serie, step by step.
    #Arguments:
        size: int, the size of the serie to generate
        p: list, the coefficients for the AR part of the model
        q: list, the coefficients for the MA part of the model
        noise: the white noise to apply to the ARMA serie. Can be a distribution name,
            a numpy random sample generator, or an array of size 'size' containing a 
            pre-computed white noise.
        noise_params: If applicable, a dictionnary containing parameters for the noise generator
    """
    #Generate a timeline and rescale the noise accordingly
    if any(e in kwargs.keys() for e in ('start_date', 'by', 'end_date')):
        # A dated timeline will be generated
        timeline, delta_t = generate_timeline(size, **kwargs)
        if 'scale' in noise_params.keys():
            noise_params['scale'] /= delta_t
    else:
        timeline, delta_t = range(size), 1 # 1 sample each unit of time by default
        
    p_order, q_order = len(p), len(q)
    max_order = max(p_order, q_order)
    #We need to invert the coefficients order to perform vectorial multiplication
    p, q = numpy.array(p)[::-1], numpy.array(q)[::-1]
    
    #We draw noise 'max_order' before the beginning of the serie (or replicate the end of the noise array)
    if isinstance(noise, str):
        noise_samples = _noise_generator(noise, size=size+max_order, param_dict=noise_params)
    elif isinstance(noise, numpy.ndarray):
        if len(noise) != size:
            raise ValueError("Noise array is not of length 'size'")
        noise_samples = numpy.append(noise[-max_order:],noise)
    else:
        try:
            noise_samples = noise(size=size+max_order, **noise_params)
        except:
            raise ValueError("Khronos don't know how to deal with {} type".format(type(noise)))
    values = numpy.array(noise_samples)
    for time in range(max_order + 1,max_order + size):
        AR_part = numpy.dot(p, values[time-p_order:time])
        MA_part = numpy.dot(q, noise_samples[time-q_order:time])
        values[time] += AR_part + MA_part

    return series_1d(values[max_order:],
                     timeline,
                     name="ARMA ({},{})".format(p_order, q_order))

def _noise_generator(distrib, size=1, param_dict={}):
    """Internal function, will return a random sample from the distribution given"""
    distrib_dict = {'gaussian':numpy.random.normal,
                    'normal':numpy.random.normal,
                    'laplace':numpy.random.laplace}
    if distrib not in distrib_dict.keys():
        raise ValueError("{} is not an available distribution shortcut for now. \
                         Please give the numpy function instead.".format(distrib))
    return distrib_dict[distrib](size=size, **param_dict)