#!/usr/bin/python3

"""
    This file contains functions that test all files in the src folder.
    Including running pep8 and the main function in the script.

    Author: Howard Cheung (howard.at@gmail.com)
    Date: 2017/03/12
"""

# import python internal libraries
import glob
import os
from subprocess import call

# import third party libraries

# import user-defined libraries


# define new functions
def test_scripts(directory: str) -> None:
    """
        This function tests all python scripts in the specfied directory.

        Inputs:
        ==========
        directory: string
            path to the directory
    """

    # fix the directory name is it is not good
    if directory[-1] != '\\' and directory[-1] != '/':
        directory = ''.join([directory, '/'])
    # get all python file in the directory, and do not test the current file
    for file in glob.glob(''.join([directory, '*.py'])):
        if os.path.realpath(file) != os.path.realpath(__file__) and (
            file.endswith(".py")
        ):
            print('Testing ', file)
            call(['pep8', file])
            call(['python', file])

# testing functions
if __name__ == '__main__':

    test_scripts('.')
