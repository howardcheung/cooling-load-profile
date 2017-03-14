#!/usr/bin/python3

"""
    This file contains functions that plot the required histograms for
    cooling load profile in operation hours

    Author: Howard Cheung (howard.at@gmail.com)
    Date: 2017/03/13
"""

# import python internal libraries
import calendar
from datetime import datetime, date
from math import ceil
import os

# import third party libraries
import matplotlib.pyplot as plt

# import user-defined modules
from plot_analysis import savefig_for_file, mkdir_if_not_exist

# global variables for plotting


# write functions
def histogram_plot(df, folder_path, col_name='CLG',
                   xlabel_name='Building Load During Operating Hours',
                   add_xlabel=' [-]', diagram_types=['pdf']):
    """
        This function plots multiple histograms for the frequency of
        occurrence of cooling load for a combination of operating chillers
        based on the percentage of full load ampere of the chillers.

        Inputs:
        ==========
        df: pandas DataFrame
            hourly data of the BMS data with datetime object as its index

        folder_path: str
            directory where the diagrams are saved

        col_name: str
            column name of the variables to be plotted. Default "kW"

        xlabel_name: str
            text at the x-axis. Default 'Part load of chiller plant'

        add_xlabel: str
            additional string to be added in the x-axis label. Default ' [-]'

        diagram_types: list
            types of diagrams to be saved. Default ['pdf']
    """

    # make directory if it is unavailable
    mkdir_if_not_exist(folder_path)

    # individual plotting function
    def _make_ind_plot(dat, duration, overall=False):
        """
            Make individual histogram plot based on the selected data and
            the specified month and year.

            Inputs:
            ==========
            dat: pandas Series
                data to be plotted

            duration: pandas Series
                length of time per data point in hours

            mn: string
                name of month to be plotted

            yr: int
                year to be plotted

            overall: bool
                if the plot involves data in a year. Override mn
        """

        # start plotting
        plt.figure(1)

        # calculate the required limits and number of bins
        max_dat = dat.max()
        delta_dat = max((10**(len(str(int(max_dat)))-2))/4, 25)
        bins = ceil(max_dat/delta_dat)

        # plot primary axis, eliminate the first bar for non-operating hours
        plt.hist(
            dat, bins=bins-1, range=(delta_dat, bins*delta_dat),
            weights=(duration/3600.0)
        )
        plt.grid(b=True, which='major', color='k', axis='y')
        plt.grid(b=True, which='major', color='k', axis='x')

        # y-axis label
        plt.ylabel('Hours of operation')

        # use the first timestamp to locate month and year
        timestamp = dat.index[0]

        # x-axis label
        if overall:
            plt.xlabel(''.join([
                xlabel_name, ' in', ' ', str(timestamp.year), add_xlabel
            ]))
            # print and show figure
            # move figure to hold everything in the diagram
            plt.subplots_adjust(top=0.9, bottom=0.2, left=0.15, right=0.9)
            savefig_for_file(''.join([
                folder_path, '/', 'histogram-CLG-', str(timestamp.year),
                '-overall'
            ]), diagram_types)
        else:
            plt.xlabel(''.join([
                xlabel_name, ' in ', timestamp.ctime()[4:7], ' ',
                str(timestamp.year), add_xlabel
            ]))
            # print and show figure
            # move figure to hold everything in the diagram
            plt.subplots_adjust(top=0.9, bottom=0.2, left=0.15, right=0.9)
            savefig_for_file(''.join([
                folder_path, '/', 'histogram-CLG-', str(timestamp.year), '-',
                '%02i' % timestamp.month
            ]), diagram_types)

    # start plotting
    yr_array = range(df.index[0].year, df.index[-1].year+1)
    for yr in yr_array:
        for mn in range(1, 13):
            # select data within the same month
            day_lim = calendar.monthrange(yr, mn)[1]
            temp_df = df.loc[
                datetime(yr, mn, 1, 0, 0):datetime(
                    yr, mn, day_lim, 23, 59
                ), :
            ]
            # check range an donly proceed if there are enough data for the
            # entire month
            try:
                if not (
                    temp_df.index[-1].date() == date(yr, mn, day_lim) and
                    temp_df.index[0].date() == date(yr, mn, 1)
                        ):
                    continue
            except IndexError:
                continue

            # make the plot with the selected data
            _make_ind_plot(temp_df[col_name], temp_df['Duration'])

        # make an overall plot for each year if data are complete
        temp_df = df.loc[
            datetime(yr, 1, 1, 0, 0):datetime(yr, 12, 31, 23, 59), :
        ]
        try:
            if not (
                temp_df.index[-1].date() == date(yr, 12, 31) and
                temp_df.index[0].date() == date(yr, 1, 1)
                    ):
                continue
        except IndexError:
            continue
        _make_ind_plot(temp_df[col_name], temp_df['Duration'], overall=True)


# testing functions
if __name__ == '__main__':

    from pathlib import Path
    import shutil

    from data_read import read_data

    # testing the dfhour_profile_plot. Can it plot?
    PDDF = read_data('../dat/load.csv', header=None)
    histogram_plot(PDDF, '../testplots', col_name='CLG',
                   xlabel_name='Building Cooling Load During Operating Hours',
                   add_xlabel=' [kW]', diagram_types=['png'])
    assert Path('../testplots/histogram-CLG-2015-overall.png').exists()
    assert not Path('../testplots/histogram-CLG-2016-overall.png').exists()
    assert not Path('../testplots/histogram-CLG-2014-overall.png').exists()
    assert Path('../testplots/histogram-CLG-2016-01.png').exists()

    print('All functions in', os.path.basename(__file__), 'are ok')
    print('Please delete plots in ../testplots/ upon completing inspection')
