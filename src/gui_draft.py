#!/usr/bin/python
"""
    This script file contains methods to define the graphical user interface
    of the tool.

    Author: Howard Cheung
    email: howard.at@gmail.com
"""

# import python internal modules
import webbrowser
from os.path import isfile

# import third party modules
import wx

# import user-defined modules
from main_analyzer import main_analyzer


# define global variables
class MainGUI(wx.Frame):
    """
        Class to hold the object for the main window of the application
    """

    def __init__(self, parent, title):
        """
            This is the initilization function for the GUI.

            Inputs:
            ==========
            parent: wx.Frame
                parent object

            title: str
                title of the window
        """
        super(MainGUI, self).__init__(
            parent, title=title, size=(550, 375)
        )  # size of the application window

        self.initui()
        self.Centre()
        self.Show()

    def initui(self):
        """
            Initialize the position of objects in the UI
        """

        # define the panel
        panel = wx.Panel(self)

        sizer = wx.GridBagSizer(6, 5)  # making a grid in your box

        # title
        # leave space at the top, left and bottom from the text to the
        # other object
        sizer.Add(
            wx.StaticText(panel, label=u'BMS data cooling load analyzer'),
            pos=(0, 0),  # position: (from top to bottom, from left to right)
            flag=wx.TOP | wx.LEFT | wx.BOTTOM,
            border=10  # border required for flag indicators
        )

        # Inputs to the data file path
        text1 = wx.StaticText(panel, label=u'Data file path:')
        sizer.Add(
            text1, pos=(1, 0), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=10
        )

        # require additional object for textbox
        # with default path
        self.tc1 = wx.TextCtrl(panel, value=u'../dat/load.csv')
        sizer.Add(
            self.tc1, pos=(1, 1), span=(1, 3), flag=wx.TOP | wx.EXPAND,
            border=10
        )
        button1 = wx.Button(panel, label=u'Browse...')
        button1.Bind(wx.EVT_BUTTON, self.OnOpen)
        sizer.Add(button1, pos=(1, 4), flag=wx.TOP | wx.RIGHT, border=10)

        # ask for existence of header as a checkbox
        text2 = wx.StaticText(panel, label=u'Existence of a header row:')
        sizer.Add(
            text2, pos=(2, 0), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=10
        )
        self.cb1 = wx.CheckBox(
            panel, pos=(20, 20)
        )
        sizer.Add(self.cb1, pos=(2, 1), flag=wx.TOP | wx.RIGHT, border=10)

        # Inputs to the directory to save the plots
        text3 = wx.StaticText(panel, label=u'Directory to save plots:')
        sizer.Add(
            text3, pos=(3, 0), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=10
        )

        # require additional object for textbox
        # with default path
        self.tc2 = wx.TextCtrl(panel, value=u'../testplots')
        sizer.Add(
            self.tc2, pos=(3, 1), span=(1, 3), flag=wx.TOP | wx.EXPAND,
            border=10
        )
        button2 = wx.Button(panel, label=u'Browse...')
        button2.Bind(wx.EVT_BUTTON, self.DirOpen)
        sizer.Add(button2, pos=(3, 4), flag=wx.TOP | wx.RIGHT, border=10)

        # Inputs to the format time string
        text4 = wx.StaticText(panel, label=u'Format time string:')
        sizer.Add(
            text4, pos=(4, 0), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=10
        )

        # require additional object for textbox
        self.tc3 = wx.TextCtrl(panel, value=u'%m/%d/%y %I:%M:%S %p CST')
        sizer.Add(
            self.tc3, pos=(4, 1), span=(1, 3), flag=wx.TOP | wx.EXPAND,
            border=10
        )

        # a button for instructions
        button_timeinstruct = wx.Button(
            panel,
            label=u'Open instructions to enter the format of the time string'
        )
        button_timeinstruct.Bind(wx.EVT_BUTTON, self.TimeInstruct)
        sizer.Add(
            button_timeinstruct, pos=(5, 1), span=(1, 2)
        )

        # Inputs to the unit of cooling load
        text5 = wx.StaticText(panel, label=u'Unit of cooling load:')
        sizer.Add(
            text5, pos=(6, 0), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=10
        )
        self.tc4 = wx.TextCtrl(panel, value=u'kW')
        sizer.Add(
            self.tc4, pos=(6, 1), span=(1, 3), flag=wx.TOP | wx.EXPAND,
            border=10
        )

        # buttons at the bottom
        button_ok = wx.Button(panel, label=u'Analysis')
        button_ok.Bind(wx.EVT_BUTTON, self.Analyzer)
        sizer.Add(button_ok, pos=(8, 4))

        # sizing of the window
        sizer.AddGrowableCol(2)  # expand to meet the window?

        panel.SetSizer(sizer)

    def ShowMessage(self):
        """
            Function to show message about the completion of the analysis
        """
        wx.MessageBox(
            u'Processing Completed', u'Status', wx.OK | wx.ICON_INFORMATION
        )

    def OnClose(self, evt):
        """
            Function to close the main window
        """
        self.Close(True)

    def OnOpen(self, evt):
        """
            Function to open a file
            Reference:
            https://wxpython.org/Phoenix/docs/html/wx.FileDialog.html
        """
        # proceed asking to the user the new directory to open
        openFileDialog = wx.FileDialog(
            self, 'Open file', '', '',
            ''.join([
                'csv files (*.csv)|*.csv;|',
                'xls files (*.xls)|*.xls;|',
                'xlsx files (*.xlsx)|*.xlsx'
            ]), wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
        )

        if openFileDialog.ShowModal() == wx.ID_CANCEL:
            return False  # the user changed idea...

        # proceed loading the file chosen by the user
        # this can be done with e.g. wxPython input streams:
        filepath = openFileDialog.GetPath()
        self.tc1.SetValue(filepath)

        if not isfile(filepath):
            wx.LogError('Cannot open file "%s".' % openFileDialog.GetPath())
            return False

    def DirOpen(self, evt):
        """
            Function to open a file
            Reference:
            https://wxpython.org/Phoenix/docs/html/wx.DirDialog.html
        """
        # proceed asking to the user the new file to open

        openDirDialog = wx.DirDialog(
            None, 'Choose directory to save the plots', '',
            wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST
        )

        if openDirDialog.ShowModal() == wx.ID_CANCEL:
            return     # the user changed idea...

        # proceed loading the file chosen by the user
        # this can be done with e.g. wxPython input streams:
        filepath = openDirDialog.GetPath()
        self.tc2.SetValue(filepath)

    def TimeInstruct(self, evt):
        """
            Function to open instructions for time string
        """
        webbrowser.open(
            u''.join([
                u'https://docs.python.org/3.5/library/datetime.html',
                u'#strftime-and-strptime-behavior'
            ])
        )

    def Analyzer(self, evt):
        """
            Function to initiate the main analysis.
        """
        # Run the analyzer
        main_analyzer(
            datafilepath=self.tc1.GetValue(),
            foldername=self.tc2.GetValue(),
            header=(1 if self.cb1.GetValue() else None),
            time_format=self.tc3.GetValue(),
            unit_name=self.tc4.GetValue()
        )

        # function to be called upon finishing processing
        wx.CallLater(0, self.ShowMessage)


# define functions
def gui_main():
    """
        Main function to intiate the GUI
    """
    app = wx.App()
    MainGUI(None, title=u'BMS data cooling load analzer')
    app.MainLoop()


# run the method for the GUI
if __name__ == '__main__':
    gui_main()
