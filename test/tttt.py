#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
from math import hypot, sin, cos, pi

class Example(wx.Frame):
  
    def __init__(self, *args, **kw):
        super(Example, self).__init__(*args, **kw) 

        self.Bind(wx.EVT_PAINT, self.OnPaint)

        self.SetSize((350, 250))
        self.SetTitle('Lines')
        self.Centre()
        self.Show(True)

    def OnPaint(self, event):
      
        dc = wx.PaintDC(self)
        size_x, size_y = self.GetClientSizeTuple()
        dc.SetDeviceOrigin(size_x/2, size_y/2)

        radius = hypot(size_x/2, size_y/2)
        angle = 0

        while (angle < 2*pi):
            x = radius*cos(angle)
            y = radius*sin(angle)
            dc.DrawLinePoint((0, 0), (x, y))
            angle = angle + 2*pi/360

def main():
    
    ex = wx.App()
    Example(None)
    ex.MainLoop()    

if __name__ == '__main__':
    main()   

