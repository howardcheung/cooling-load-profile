﻿#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    This script file contains methods to define the graphical user interface
    of the tool.

    Author: Howard Cheung
    email: howard.at@gmail.com
"""

import wx

class Example(wx.Frame):

    def __init__(self, parent, title):    
        super(Example, self).__init__(parent, title=title, 
            size=(450, 300))  # size of the application window

        self.InitUI()
        self.Centre()
        self.Show()     

    def InitUI(self):
      
        panel = wx.Panel(self)
        
        sizer = wx.GridBagSizer(5, 5)  # making a grid in your box

        # title
        sizer.Add(
            wx.StaticText(panel, label="BMS data cooling load analyzer"),
            pos=(0, 0),  # position: (from top to bottom, from left to right)
            flag=wx.TOP|wx.LEFT|wx.BOTTOM,  # leave space at the top, left and bottom from the text to the other object
            border=10  # border required for flag indicators
        )

        # Inputs to the data file path
        text1 = wx.StaticText(panel, label="Data file path:")
        sizer.Add(text1, pos=(1, 0), flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=10)

        tc1 = wx.TextCtrl(panel)  # require additional object for textbox
        sizer.Add(tc1, pos=(1, 1), span=(1, 3), flag=wx.TOP|wx.EXPAND, border=10)

        button1 = wx.Button(panel, label="Browse...")
        sizer.Add(button1, pos=(1, 4), flag=wx.TOP|wx.RIGHT, border=10)

        # Inputs to the directory to save the plots
        text2 = wx.StaticText(panel, label="Directory to save plots:")
        sizer.Add(text2, pos=(2, 0), flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=10)

        tc2 = wx.TextCtrl(panel)  # require additional object for textbox
        sizer.Add(tc2, pos=(2, 1), span=(1, 3), flag=wx.TOP|wx.EXPAND, border=10)

        button2 = wx.Button(panel, label="Browse...")
        sizer.Add(button2, pos=(2, 4), flag=wx.TOP|wx.RIGHT, border=10)

        # Inputs to the format time string
        text3 = wx.StaticText(panel, label="Format time string:")
        sizer.Add(text3, pos=(3, 0), flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=10)

        tc3 = wx.TextCtrl(panel)  # require additional object for textbox
        sizer.Add(tc3, pos=(3, 1), span=(1, 3), flag=wx.TOP|wx.EXPAND, border=10)

        # Inputs to the unit of cooling load
        text4 = wx.StaticText(panel, label="Unit of cooling load:")
        sizer.Add(text4, pos=(4, 0), flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=10)

        tc4 = wx.TextCtrl(panel)  # require additional object for textbox
        sizer.Add(tc4, pos=(4, 1), span=(1, 3), flag=wx.TOP|wx.EXPAND, border=10)

        # buttons at the bottom
        button_ok = wx.Button(panel, label="Ok")
        sizer.Add(button_ok, pos=(6, 3))

        button_cancel = wx.Button(panel, label="Cancel")
        sizer.Add(button_cancel, pos=(6, 4), span=(1, 1),  
            flag=wx.BOTTOM|wx.RIGHT, border=5)

        # sizing of the window
        sizer.AddGrowableCol(2)  # expand to meet the window?
        
        panel.SetSizer(sizer)


if __name__ == '__main__':
  
    app = wx.App()
    Example(None, title="BMS data cooling load analzer")
    app.MainLoop()