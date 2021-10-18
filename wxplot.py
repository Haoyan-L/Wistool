# coding: utf-8
'''
Created on 2018年9月29日
@author: lili
@revision: hli30
'''
from wx import ID_ANY
from wx import BLUE
from wx import Panel
from wx import ScrolledWindow
from wx import Pen
from wx.lib import plot as wxplot


class PlotExample(Panel):
    def __init__(self, parent, csize):
        Panel.__init__(self, parent=parent, id=ID_ANY, size=csize)
        self.scroll = ScrolledWindow(self, -1, size=(400, 400))
        self.scroll.SetScrollbars(1, 10, 1, csize[1] / 10)
        self.pc = wxplot.PlotCanvas(self.scroll, size=csize)
        self.pc.canvas.Size = csize

        # Edit panel-wide settings
        axes_pen = Pen(BLUE, 1)
        self.pc.axesPen = axes_pen
        self.pc.enableAxes = (True, True, True, True)
        self.pc.enableAxesValues = (True, True, True, False)
        self.pc.enableTicks = (True, True, True, False)

    #         self.pc.showScrollbars=True
    #         self.pc._ticks(20, 70, 5)

    def plot(self, xx, yy):
        # Generate some Data
        x_data = xx
        y_data = yy

        # most items require data as a list of (x, y) pairs:
        #    [[1x, y1], [x2, y2], [x3, y3], ..., [xn, yn]]
        xy_data = list(zip(x_data, y_data))

        # Create your Poly object(s).
        # Use keyword args to set display properties.
        line = wxplot.PolySpline(xy_data, colour='red')

        # create your graphics object
        graphics = wxplot.PlotGraphics([line])
        # draw the graphics object on the canvas
        self.pc.Draw(graphics)
        self.pc.Update()
