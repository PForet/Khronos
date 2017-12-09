from matplotlib import pyplot as plt

def plot_ts(series_1d_,style='classic'):
    """Plot a serie using pyplot. Will deal with train/test split if available
    #Argument:
        style: string or list of strings, pyplot style(s) to use if needed"""

    if not series_1d_._splitted:
        with plt.style.context(style):
            plt.plot(series_1d_.timeline, series_1d_.values, '-x')
    
    else:
        try:
            _ = series_1d_._last_val_index
        except:
            _ = False
            
        tmp_serie = series_1d_.get_train()
        with plt.style.context(style):
            plt.plot(tmp_serie.timeline, tmp_serie.values, '-x', label='Training points')
            
        tmp_serie = series_1d_.get_test(include_last=True)
        with plt.style.context(style):
            plt.plot(tmp_serie.timeline, tmp_serie.values, '-x', label='Testing points')
        
        if _:
            tmp_serie = series_1d_.get_val(include_last=True)
            with plt.style.context(style):
                plt.plot(tmp_serie.timeline, tmp_serie.values, '-x', label='Validation points')
                
    with plt.style.context(style):
        if series_1d_.name is not None:
            plt.ylabel(series_1d_.name)
        plt.legend()
    plt.show()
