#!/usr/bin/python3

"""
    This file contains functions that plots time series data box plots
    for cooling load on weekdays

    Author: Howard Cheung (howard.at@gmail.com)
    Date: 2017/03/12
"""

# import libraries
from datetime import datetime
import os
import pathlib
import random

# import third party libraries
from matplotlib.ticker import MultipleLocator
import pandas as pd
import pylab as plt

# import user-defined libraries
from plot_analysis import savefig_for_file, mkdir_if_not_exist


# write functions
def dfhour_profile_plot(df, folder_path, col_name='kW',
                        y_label='Average building power consumption [kW]',
                        showfliers=True, diagram_types=['png']):
    """
        This function plots the hourly kVA and kWh profiles of weekdays every
        month in terms of box plots

        Inputs:
        ==========
        df: pandas DataFrame
            hourly data of the BMS data with datetime object as its index

        folder_path: str
            directory where the diagrams are saved

        col_name: str
            column name of the variables to be plotted. Default "kW"

        y_label: str
            Label on y-axis. Default
            "Average building power consumption [kW]"

        showfliers: bool
            if the box plot should show outliers. Default True

        diagram_types: list
            types of diagrams to be saved. Default ['pdf']
    """

    # make directory if it is unavailable
    mkdir_if_not_exist(folder_path)

    # prepare array of time
    times = []
    times.append(df.index[0].time())
    while df.index[len(times)].time() != times[0]:
        times.append(df.index[len(times)].time())

    # use one plot as an example for now
    # random number for fig number
    fig_num = int(random.random()*1000.0)
    yr_array = range(df.index[0].year, df.index[-1].year+1)
    for yr in yr_array:
        for mn in range(1, 13):
            for load_type in ['wkdy']:
                # initialize
                data = []
                # select data
                max_value = 0.0
                for time in times:
                    data.append(
                        df.loc[
                            [
                                (
                                    dy.weekday() <= 4 if load_type == 'wkdy'
                                    else dy.weekday() == (
                                        5 if load_type == 'sat' else 6
                                    )
                                ) and dy.time() == time and
                                dy.month == mn and dy.year == yr
                                for dy in df.index
                            ], col_name
                        ]
                    )
                    max_value = max(max_value, data[-1].max())
                # skip plot if the size of data array is insufficient
                if len(data[0]) < 27:
                    continue
                # create box plot
                plt.figure(mn*fig_num)
                ax = plt.subplot(111)
                plt.boxplot(data, labels=[
                    time.strftime('%H:%M') if time.minute == 0 else ''
                    for time in times
                ], showfliers=showfliers)
                # set axis label
                timestamp = df.loc[[
                    dy.month == mn for dy in df.index
                ], :].index[0]
                plt.xlabel(''.join([
                    'Time on ', (
                        'weekdays' if load_type == 'wkdy' else (
                            'Saturdays' if load_type == 'sat' else 'Sundays'
                        )
                    ), ' in ', timestamp.ctime()[4:7], ' ', str(yr)
                ]))
                plt.ylabel(y_label)
                # set minor grid line
                minorLocator = MultipleLocator(
                    (0.025 if max_value < 2.0 else 100)
                    if max_value <= 2000.0 else 2.5*10**(
                        len(str(int(max_value)))-2
                    )
                )
                ax.yaxis.set_minor_locator(minorLocator)
                majorLocator = MultipleLocator(
                    (0.05 if max_value < 2.0 else 200)
                    if max_value <= 2000.0 else 5.0*10**(
                        len(str(int(max_value)))-2
                    )
                )
                ax.yaxis.set_major_locator(majorLocator)
                plt.grid(b=True, which='major', color='k', axis='y')
                # rotate x-axis labels
                locs, labels = plt.xticks()
                plt.setp(labels, rotation=90)
                # create more space for x-axis labels
                plt.subplots_adjust(top=0.95, bottom=0.2)
                # set minimum for y-axis as zero
                if max_value > 2.0:
                    ax.set_ylim([0, None])
                else:
                    ax.set_ylim([0.8, 1.1])
                # save plots
                savefig_for_file(''.join([
                   folder_path, '/', load_type, '-load-profile-',
                   col_name, '-', '%04i' % yr, '-', '%02i' % mn
                ]), diagram_types)


# test functions
if __name__ == '__main__':

    from pathlib import Path
    import shutil

    from data_read import read_data

    # testing the dfhour_profile_plot. Can it plot?
    PDDF = read_data('../dat/load.csv', header=None)
    dfhour_profile_plot(PDDF, '../testplots', col_name='CLG',
                        y_label='Instantaneous building cooling load [kW]',
                        showfliers=True, diagram_types=['png'])
    assert Path('../testplots/wkdy-load-profile-CLG-2015-01.png').exists()
    assert Path('../testplots/wkdy-load-profile-CLG-2016-01.png').exists()
    assert not Path('../testplots/wkdy-load-profile-CLG-2014-01.png').exists()

    print('All functions in', os.path.basename(__file__), 'are ok')
