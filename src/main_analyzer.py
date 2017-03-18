#!/usr/bin/python3

"""
    This file contains functions that govern the input and output structure of
    the software

    Author: Howard Cheung (howard.at@gmail.com)
    Date: 2017/03/18
"""

# import python internal libraries

# import third party libraries

# import user-defined modules
from data_read import read_data
from plot_wkdyseries import dfhour_profile_plot
from plot_histograms import histogram_plot

# global variables for plotting


# write functions
def main_analyzer(datafilepath: str, foldername: str='./testplots',
                  header: int=None,
                  time_format: str='%m/%d/%y %I:%M:%S %p CST',
                  unit_name: str='kW'):
    """
        This function reads the data and put plots in the
        specified directory.

        Inputs:
        ==========
        datafilepath: string
            path to the data file

        folder_path: str
            directory where the diagrams are saved

        header: int, list of ints, default None
            Row (0-indexed) to use for the column labels of the parsed
            DataFrame. If a list of integers is passed those row positions
            will be combined into a MultiIndex. Default None

        time_format: string
            format of string in time. Default '%m/%d/%y %I:%M:%S %p CST'
            Please check https://docs.python.org/3.5/library/datetime.html#strftime-and-strptime-behavior
            for details

        unit_name: string
            unit of the data. Default 'kW'
    """

    pddf = read_data(datafilepath, header)
    dfhour_profile_plot(pddf, foldername, col_name='CLG',
                        y_label=''.join([
                            'Instantaneous building cooling load [', unit_name,
                            ']'
                        ]),
                        showfliers=True, diagram_types=['png'])
    histogram_plot(pddf, foldername, col_name='CLG',
                   xlabel_name='Building Cooling Load During Operating Hours',
                   add_xlabel=''.join([' [', unit_name, ']']),
                   diagram_types=['png'])


# testing functions
if __name__ == '__main__':

    import os
    from pathlib import Path
    import shutil

    if Path('../testplots').exists():
        shutil.rmtree('../testplots')
    main_analyzer('../dat/load.csv', '../testplots')
    assert Path('../testplots/wkdy-load-profile-CLG-2015-01.png').exists()
    assert Path('../testplots/wkdy-load-profile-CLG-2016-01.png').exists()
    assert not Path('../testplots/wkdy-load-profile-CLG-2014-01.png').exists()
    assert Path('../testplots/histogram-CLG-2015-overall.png').exists()
    assert not Path('../testplots/histogram-CLG-2016-overall.png').exists()
    assert not Path('../testplots/histogram-CLG-2014-overall.png').exists()
    assert Path('../testplots/histogram-CLG-2016-01.png').exists()
    print('All functions in', os.path.basename(__file__), 'are ok')
    print('Please delete plots in ../testplots/ upon completing inspection')
    