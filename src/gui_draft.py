#!/usr/bin/python
"""
    This script file contains methods to define the graphical user interface
    of the tool.

    Author: Howard Cheung
    email: howard.at@gmail.com
"""

# import python internal modules

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
            parent, title=title, size=(500, 350)
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

        sizer = wx.GridBagSizer(5, 5)  # making a grid in your box

        # title
        # leave space at the top, left and bottom from the text to the
        # other object
        sizer.Add(
            wx.StaticText(panel, label='BMS data cooling load analyzer'),
            pos=(0, 0),  # position: (from top to bottom, from left to right)
            flag=wx.TOP | wx.LEFT | wx.BOTTOM,
            border=10  # border required for flag indicators
        )

        # Inputs to the data file path
        text1 = wx.StaticText(panel, label="Data file path:")
        sizer.Add(
            text1, pos=(1, 0), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=10
        )

        # require additional object for textbox
        # with default path
        self.tc1 = wx.TextCtrl(panel, value='../dat/load.csv')
        sizer.Add(
            self.tc1, pos=(1, 1), span=(1, 3), flag=wx.TOP | wx.EXPAND,
            border=10
        )

        button1 = wx.Button(panel, label="Browse...")
        sizer.Add(button1, pos=(1, 4), flag=wx.TOP | wx.RIGHT, border=10)

        # ask for existence of header as a checkbox
        text2 = wx.StaticText(panel, label='Existence of header:')
        sizer.Add(
            text2, pos=(2, 0), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=10
        )
        self.cb1 = wx.CheckBox(
            panel, pos=(20, 20)
        )
        sizer.Add(self.cb1, pos=(2, 1), flag=wx.TOP | wx.RIGHT, border=10)

        # Inputs to the directory to save the plots
        text3 = wx.StaticText(panel, label="Directory to save plots:")
        sizer.Add(
            text3, pos=(3, 0), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=10
        )

        # require additional object for textbox
        # with default path
        self.tc2 = wx.TextCtrl(panel, value='../testplots')
        sizer.Add(
            self.tc2, pos=(3, 1), span=(1, 3), flag=wx.TOP | wx.EXPAND,
            border=10
        )

        button2 = wx.Button(panel, label="Browse...")
        sizer.Add(button2, pos=(3, 4), flag=wx.TOP | wx.RIGHT, border=10)

        # Inputs to the format time string
        text4 = wx.StaticText(panel, label="Format time string:")
        sizer.Add(
            text4, pos=(4, 0), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=10
        )

        # require additional object for textbox
        self.tc3 = wx.TextCtrl(panel, value='%m/%d/%y %I:%M:%S %p CST')
        sizer.Add(
            self.tc3, pos=(4, 1), span=(1, 3), flag=wx.TOP | wx.EXPAND,
            border=10
        )

        # Inputs to the unit of cooling load
        text5 = wx.StaticText(panel, label="Unit of cooling load:")
        sizer.Add(
            text5, pos=(5, 0), flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=10
        )
        self.tc4 = wx.TextCtrl(panel, value='kW')
        sizer.Add(
            self.tc4, pos=(5, 1), span=(1, 3), flag=wx.TOP | wx.EXPAND,
            border=10
        )

        # buttons at the bottom
        button_ok = wx.Button(panel, label="Analysis")
        button_ok.Bind(wx.EVT_BUTTON, self.analyzer)
        sizer.Add(button_ok, pos=(7, 4))

        # button to close the box
        # button_cancel = wx.Button(panel, label="Cancel")
        # button_cancel.Bind(wx.EVT_BUTTON, self.onclose)
        # sizer.Add(
        #    button_cancel, pos=(7, 4), span=(1, 1),
        #    flag=wx.BOTTOM | wx.RIGHT, border=5
        # )

        # sizing of the window
        sizer.AddGrowableCol(2)  # expand to meet the window?

        panel.SetSizer(sizer)

    def showmessage(self):
        """
            Function to show message about the completion of the analysis
        """
        wx.MessageBox(
            'Processing Complete', 'Info', wx.OK | wx.ICON_INFORMATION
        )

    def onclose(self, evt):
        """
            Function to close the main window
        """
        self.Close(True)

    def analyzer(self, evt):
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
        wx.CallLater(0, self.showmessage)

def main():
    """
        Main function to intiate the GUI
    """
    app = wx.App()
    MainGUI(None, title="BMS data cooling load analzer")
    app.MainLoop()

# run the method for the GUI
if __name__ == '__main__':
    main()
