#!/usr/bin/python3

"""
    This file contains utility functions for making plots

    Author: Howard Cheung (hcheun@polyu.edu.hk)
    Date: 2016/01/19
"""

# import python internal libraries
from datetime import timedelta
import itertools
from math import isnan
from os import mkdir
from pathlib import Path

# import third party libraries
from matplotlib.pyplot import xlabel, xticks, setp, savefig, clf


# global variables for plotting
LineStyles = ['-', ':', '-.', '--']*5
LineWidths = [a for a in itertools.chain.from_iterable([
    [1+2*x]*4 for x in range(5)
])]


# write functions
def mkdir_if_not_exist(usrpath):
    """
        Make a directory at usrpath if the directory does not exist

        Inputs:
        ==========
        usrpath: str
            position of the path
    """

    if not Path(usrpath).exists():
        mkdir(usrpath)


def set_date_for_xaxis():
    """
        Function to set the dates on x-axis appropriately
    """
    xlabel('Date')
    locs, labels = xticks()
    setp(labels, rotation=90)


def savefig_for_file(filename: str, diagram_types: list=['pdf'],
                     dpi: float=300):
    """
        Function to save diagram files in .eps, .pdf and .png format.
        Show the plot and clear the current figure after saving operation.

        Inputs:
        ==========
        filename: string
            path to the file. Note that the folders should be created
            beforehand

        diagram_types: list
            types of diagrams to be saved. Default ['pdf']

        dpi: float
            dpi for diagram. Default 300
    """

    for ext in diagram_types:
        savefig(
            '.'.join([filename, ext]), dpi=300, format=ext, frameon=False
        )
    clf()


def list_get_legend_handles_labels(list_of_axes: list):
    """
        Function to flatten list of handles and legends from AxesSubplot
        objects

        Inputs:
        ========
        list_of_axes: list of matplotlib.axes.Axes
            list of axes objects in the same plot to be documented
            by legend
    """

    handles = []
    labels = []
    for axes in list_of_axes:
        h, l = axes.get_legend_handles_labels()
        handles += h
        labels += l
    return handles, labels


# testing functions
if __name__ == '__main__':

    from os.path import basename
    from shutil import rmtree

    # testing the make directory function mkdif_if_not_exist
    mkdir_if_not_exist('./testtesttest/')
    assert Path('./testtesttest/').exists()
    rmtree('./testtesttest/')

    print('All functions in', basename(__file__), 'are ok')
