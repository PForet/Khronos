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
    values = numpy.random.normal(scale=scale*numpy.sqrt(delta_t), size=size)
    return series_1d(values, timeline)

    
        