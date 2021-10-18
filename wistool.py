# import os
#pyinstaller -w wistool.py --exclude-module matplotlib
import sys

import img
# import wx
import wx.grid
from wx.adv import AboutDialogInfo, AboutBox
from wx.grid import Grid
from wx.xrc import *
from wishelper import *
import datetime

from wxplot import PlotExample

import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
TBFLAGS = (wx.TB_HORIZONTAL
           | wx.NO_BORDER
           | wx.TB_FLAT
           | wx.TB_TEXT
           # | wx.TB_HORZ_LAYOUT
           )


class myapp(wx.App):
    def __init__(self, argv=None):
        self.fnm = None

        if argv is not None and len(argv) > 1:
            self.fnm = argv[1]
            self.statub.SetStatusText('')
        #             for arg in argv:
        #                 print arg
        wx.App.__init__(self)

    def OnInit(self):
        # self.apppath=sys.argv[0]
        self.apppath, appfilename = os.path.split(os.path.abspath(sys.argv[0]))
        # print(dirname,filename)
        if os.path.isdir(self.apppath):
            self.apppath = self.apppath + '\\'
        # print(self.apppath)
        self.res = XmlResource(self.apppath + 'reer.xrc')
        self.frame = self.res.LoadFrame(None, 'ID_WXFRAME')
        self.frame.SetIcon(img.oszillograph.Icon)
        self.frame.SetSize((800, 600))
        # self.frame.SetTitle('WIS工具')
        self.notebk = XRCCTRL(self.frame, 'ID_NOTEBOOK')
        self.channelwin = XRCCTRL(self.notebk, 'ID_channel')
        self.channelpanel = XRCCTRL(self.notebk, 'ID_PANEL')
        self.listchannel = XRCCTRL(self.notebk, 'ID_LISTBOX')
        self.listflow = XRCCTRL(self.notebk, 'ID_LISTBOX1')
        self.listtable = XRCCTRL(self.notebk, 'ID_LISTBOX2')
        self.viewflow = XRCCTRL(self.notebk, 'ID_TEXTCTRL')
        self.viewtab = XRCCTRL(self.notebk, 'ID_GRID')
        self.viewtab.EnableEditing(False)
        self.frame.Bind(wx.EVT_LISTBOX, self.showflow, id=XRCID('ID_LISTBOX1'))
        self.frame.Bind(wx.EVT_LISTBOX, self.showtable, id=XRCID('ID_LISTBOX2'))
        self.frame.Bind(wx.EVT_LISTBOX, self.showchannel, id=XRCID('ID_LISTBOX'))

        self.notebk.SetPageText(0,'Tracks')
        self.notebk.SetPageText(1,'Flow Data')
        self.notebk.SetPageText(2,'Table Data')
        self.actch_data = None
        self.act_filename = ""
        self.AddToolbar()
        dt = MyFileDropTarget(self)
        self.frame.SetDropTarget(dt)
        self.frame.Show()
        self.wish = None
        # print os.environ
        if self.fnm:
            self.openWisfile(self.fnm)
        return True

    def AddToolbar(self):

        self.toolb = self.frame.CreateToolBar(TBFLAGS)
        self.statub = self.frame.CreateStatusBar(2)
        self.statub.SetStatusText("")
        tsize = (28, 28)
        self.toolb.SetToolBitmapSize(tsize)

        openimg = img.folder.Image
        expimg = img.export1.Image
        explasimg = img.export1.Image
        exp4petrel = img.conversion.Image
        savimg = img.disk_yellow.Image
        aboimg = img.about.Image

        self.toolb.AddTool(100, 'Single WIS', openimg.ConvertToBitmap(), wx.NullBitmap, wx.ITEM_NORMAL,
                           shortHelp="Open single WIS file",
                           longHelp="Open single WIS file")
        self.toolb.AddSeparator()
        # self.tsav = self.toolb.AddTool(200, ' 保存 ', savimg.ConvertToBitmap(), wx.NullBitmap, wx.ITEM_NORMAL,
        #                              shortHelp="保存文件", longHelp="保存文件")
        self.tsav = self.toolb.AddTool(200, ' Save Trajectory ', savimg.ConvertToBitmap(), wx.NullBitmap, wx.ITEM_NORMAL,
                                       shortHelp="Save trajectory", longHelp="Save trajectory")

        self.toolb.AddTool(300, 'Output TXT', expimg.ConvertToBitmap(), wx.NullBitmap, wx.ITEM_NORMAL,
                           shortHelp="WIS to TXT", longHelp="WIS to TXT")
        self.toolb.AddTool(400, 'Output LAS', explasimg.ConvertToBitmap(), wx.NullBitmap, wx.ITEM_NORMAL,
                           shortHelp="WIS to LAS",
                           longHelp="WIS to LAS")
        self.toolb.AddSeparator()
        self.toolb.AddTool(500, 'Batch Output', exp4petrel.ConvertToBitmap(), wx.NullBitmap, wx.ITEM_NORMAL,
                           shortHelp="Output trajectory, logging and wellhead XY",
                           longHelp="Output trajectory, logging and wellhead XY")
        self.toolb.AddSeparator()
        self.toolb.AddTool(600, 'About', aboimg.ConvertToBitmap(), wx.NullBitmap, wx.ITEM_NORMAL, shortHelp="About",
                           longHelp="About")
        self.toolb.Realize()

        # tb.AddTool(20, "Open", open_bmp, shortHelpString ="Open", longHelpString="Long help for 'Open'")
        self.Bind(wx.EVT_TOOL, self.OnOpenTool, id=100)
        self.Bind(wx.EVT_TOOL, self.OnSaveTraj, id=200)
        self.Bind(wx.EVT_TOOL, self.OnSaveTXT, id=300)
        self.Bind(wx.EVT_TOOL, self.OnSaveLAS, id=400)
        self.Bind(wx.EVT_TOOL, self.OnSavePTL, id=500)
        self.Bind(wx.EVT_TOOL, self.AboutMe, id=600)

    def showflow(self, evt):
        self.statub.SetStatusText('')
        self.viewflow.SetValue(self.wish.readflow(evt.GetString()))
        self.toolb.SetToolShortHelp(200, u'save flow data[' + evt.GetString() + ']')
        # sav=self.toolb.FindById(200)
        # self.tsav.SetLabel('保存流数据['+evt.GetString()+']')
        # self.toolb.Realize()

    def showtable(self, evt):
        self.statub.SetStatusText('')
        self.viewtab.ClearGrid()
        tabdata = self.wish.readtable(evt.GetString())
        # print(len(tabdata[0]))
        if len(tabdata[0]) > 0:
            gtable = CustomDataTable()
            gtable.colLabels = tabdata[0]
            gtable.data = tabdata[1:]
            self.viewtab.SetTable(gtable, True)
            self.viewtab.ForceRefresh()
            self.toolb.SetToolShortHelp(200, u'save table data[' + evt.GetString() + ']')
            # self.toolb.FindById(200).SetLabel('保存表数据['+evt.GetString()+']')
            # self.toolb.Realize()

    def showchannel(self, evt):
        self.statub.SetStatusText('')
        self.createchannelwin(evt.GetString())

    def createchannelwin(self, chn):
        newspwin = wx.SplitterWindow(self.channelwin, wx.ID_ANY, style=wx.SP_3DBORDER | wx.SP_3DSASH | wx.NO_BORDER,
                                     size=(100, 100))
        xgrid = Grid(newspwin, wx.ID_ANY, style=wx.SUNKEN_BORDER)
        xgrid.SetRowLabelSize(0)
        xtable = CustomDataTable()
        xtable.colLabels = ['DEPT', chn]
        xx, yy = self.wish.readchannel(chn)
        self.actch_data = (xx, yy)
        xtable.data = list(zip(xx[:500], yy[:500]))
        xgrid.SetTable(xtable, True)
        xgrid.ForceRefresh()

        xpan = wx.Panel(newspwin, wx.ID_ANY, style=wx.SUNKEN_BORDER, size=(300, 4000))
        self.toolb.SetToolShortHelp(200, u'Save log data[' + chn + ']')
        mpl = PlotExample(xpan, (400, 4000))
        mpl.pc.xSpec = (0, max(filter(lambda x: x > -999, yy)) + 0.1)
        mpl.plot(yy, xx * (-1))
        BoxSizer = wx.BoxSizer(wx.VERTICAL)
        BoxSizer.Add(mpl, proportion=1, border=1, flag=wx.EXPAND | wx.ALL)
        xpan.SetSizer(BoxSizer)
        xpan.Fit()

        newspwin.SetMinimumPaneSize(20)
        newspwin.SplitVertically(xgrid, xpan, 200)
        old = self.channelwin.GetWindow2()
        self.channelwin.ReplaceWindow(old, newspwin)
        old.Destroy()
        newspwin.Show(True)

    def OnOpenTool(self, evt):
        self.statub.SetStatusText('')
        filDlg = wx.FileDialog(self.frame, 'Select WIS file', wildcard="WIS file (*.wis)|*.wis")
        if filDlg.ShowModal() == wx.ID_OK:
            self.OnInit
            self.act_filename = filDlg.GetPath()
            self.openWisfile(self.act_filename)
        filDlg.Destroy()

    # def OnSaveTool(self, evt):
    #     #     self.statub.SetStatusText('')
    #     #     pg = self.notebk.GetSelection()
    #     #     if pg == 1:
    #     #         stda = self.viewflow.GetValue()
    #     #         filDlg = wx.FileDialog(self.frame, '保存流', defaultFile=self.listflow.GetStringSelection(),
    #     #                                wildcard="TXT文件 (*.txt)|*.txt", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
    #     #         if filDlg.ShowModal() == wx.ID_OK:
    #     #             flname = filDlg.GetPath()
    #     #             if not os.path.splitext(flname)[1]:  # 如果没有文件名后缀
    #     #                 flname = flname + '.txt'
    #     #             self.SaveFile(flname, stda)
    #     #         filDlg.Destroy()
    #     #     elif pg == 2:
    #     #         tabdata = {}
    #     #         for tab in self.listtable.Strings:
    #     #             tabdata[tab] = self.wish.readtable(tab)
    #     #
    #     #         filDlg = wx.FileDialog(self.frame, '保存表', defaultFile='table', wildcard="Excel文件 (*.xls)|*.xls",
    #     #                                style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
    #     #         if filDlg.ShowModal() == wx.ID_OK:
    #     #             flname = filDlg.GetPath()
    #     #             if not os.path.splitext(flname)[1]:  # 如果没有文件名后缀
    #     #                 flname = flname + '.xls'
    #     #             pxls.savedata(flname, tabdata)
    #     #         filDlg.Destroy()
    #     #     else:
    #     #         tabdata = {}
    #     #         chn = self.listchannel.GetStringSelection()
    #     #         if self.actch_data:
    #     #             tabdata[chn] = list(zip(self.actch_data[0], self.actch_data[1]))
    #     #             tabdata[chn].insert(0, ('深度', chn))
    #     #
    #     #         filDlg = wx.FileDialog(self.frame, '保存通道', defaultFile=chn, wildcard="Excel文件 (*.xls)|*.xls",
    #     #                                style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
    #     #         if filDlg.ShowModal() == wx.ID_OK:
    #     #             flname = filDlg.GetPath()
    #     #             if not os.path.splitext(flname)[1]:  # 如果没有文件名后缀
    #     #                 flname = flname + '.xls'
    #     #             pxls.savedata(flname, tabdata)
    #     #         filDlg.Destroy()

    def OnSaveTraj(self, evt):
        self.statub.SetStatusText('')
        if self.wish:
            self.wish.save2traj(os.path.splitext(self.act_filename)[0] + '.txt')
            self.statub.SetStatusText("Saved to " + os.path.splitext(self.act_filename)[0] + '.txt')

    # def SaveFile(self, fn, st):
    #     self.statub.SetStatusText('')
    #     f = open(fn, 'w')
    #     f.write(st)
    #     f.close()

    def OnSaveTXT(self, evt):
        self.statub.SetStatusText('')
        if self.wish:
            [errtrack, errdepth] = self.wish.channel2txt(os.path.splitext(self.act_filename)[0] + '.txt')
            self.statub.SetStatusText("Saved to " + os.path.splitext(self.act_filename)[0] + '.txt')
            if len(errtrack) > 0:
                wx.MessageBox("The depth and track might be shifted\n"
                              + errtrack.replace(",", "  ") + "\n"
                              + errdepth.replace(",", "  ") + "\n"
                              + "m，which has been modified", caption="Warning")

    def OnSaveLAS(self, evt):
        self.statub.SetStatusText('')
        if self.wish:
            [errtrack, errdepth] = self.wish.channel2las(os.path.splitext(self.act_filename)[0] + '.las')
            self.statub.SetStatusText("Saved to" + os.path.splitext(self.act_filename)[0] + '.las')
            if len(errtrack) > 0:
                wx.MessageBox("The depth and track might be shifted\n"
                              + errtrack.replace(",", "  ") + "\n"
                              + errdepth.replace(",", "  ") + "\n"
                              + "m，which has been modified", caption="Warning")

    def OnSavePTL(self, evt):
        self.statub.SetStatusText('')
        errwell = []
        errtrack = []
        errdepth = []
        errmsg = ""
        filDlg = wx.FileDialog(self.frame, 'Select WIS file', wildcard="WIS file (*.wis)|*.wis", style=wx.FD_OPEN | wx.FD_MULTIPLE)
        if filDlg.ShowModal() == wx.ID_OK:
            self.act_filename = filDlg.GetPaths()
            coordfn = os.path.dirname(self.act_filename[0]) + "\\WIS_Coord_" + datetime.datetime.now().strftime(
                '%m%d%H%M') + ".csv"
            filDlg.Destroy()
            pgs = 1
            self.frame.SetCursor(wx.Cursor(wx.CURSOR_WAIT))
            for fn in self.act_filename:
                self.statub.SetStatusText("Converting......" + str(pgs) + "/" + str(len(self.act_filename)), 1)
                self.openWisfile(fn)
                [t, d] = self.wish.channel2las(os.path.splitext(fn)[0] + '.las')  # out put las and trajectory
                if len(t) > 0:
                    errtrack.append(t)
                    errdepth.append(d)
                self.wish.save2traj(os.path.splitext(fn)[0] + '.txt')
                temp = self.wish.savecoord(coordfn)
                if len(t) > 0:
                    errwell.append(temp)
                pgs += 1
            self.statub.SetStatusText(str(len(self.act_filename)) + "wells' data has been saved to correspondent folder")
            self.statub.SetStatusText("" ,1)
            self.frame.SetCursor(wx.Cursor(wx.CURSOR_ARROW))
            if len(errwell) > 0:
                for wn in range(0, len(errwell)):
                    errmsg = errmsg + \
                             errwell[wn] + " \n" \
                             + errtrack[wn].replace(",", "  ") + "\n" \
                             + errdepth[wn].replace(",", "  ") + '\n'
                wx.MessageBox("The depth and track of following items might be shifted：\n" + errmsg, caption="Warning")

    def AboutMe(self, evt):
        self.statub.SetStatusText('')
        info = AboutDialogInfo()
        info.SetName("WIS logging toolbox")
        info.SetVersion("2.0 ")
        info.SetDescription("This tool can be used to check the .wis logging file.\n"
                            "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
                            "2.0 Upgrade:\n"
                            "    1. revised code for log display and conversion\n"
                            "    2. add support to las format\n"
                            "    3. add batch conversion mode")
        info.SetCopyright("(C) 2014 liliang <ll4_cq@petrochina.com.cn>\n(C) 2020 lihaoyan <hli30@slb.com>")

        AboutBox(info)

    def openWisfile(self, finame):
        self.statub.SetStatusText('')
        self.wish = wishelper(open(finame, "rb"))
        # print(self.wish.headerinfo)
        # print([xx for xx in self.wish.flowlist])
        self.listflow.Set(sorted(self.wish.flowlist.keys()))
        self.listchannel.Set(sorted(self.wish.channellist.keys()))
        self.listtable.Set(sorted(self.wish.tablelist.keys()))
        # print self.wish.tablelist

    def setgridlabel(self, labs):
        y = 0
        for lv in labs:
            self.viewtab.SetColLabelValue(y, lv)
            y = y + 1


class CustomDataTable(wx.grid.GridTableBase):
    def __init__(self):
        wx.grid.GridTableBase.__init__(self)
        self.colLabels = []
        self.data = []

    # --------------------------------------------------
    # required methods for the wxPyGridTableBase interface

    def GetNumberRows(self):
        return len(self.data)

    def GetNumberCols(self):
        return len(self.data[0])

    def IsEmptyCell(self, row, col):
        try:
            return not self.data[row][col]
        except IndexError:
            return True

    # Get/Set values in the table.  The Python version of these
    # methods can handle any data-type, (as long as the Editor and
    # Renderer understands the type too,) not just strings as in the
    # C++ version.
    def GetValue(self, row, col):
        try:
            return self.data[row][col]
        except IndexError:
            return ''

    def SetValue(self, row, col, value):
        def innerSetValue(row, col, value):
            try:
                if value == None:
                    value = ''
                self.data[row][col] = value
            except IndexError:
                # add a new row
                self.data.append([''] * self.GetNumberCols())
                innerSetValue(row, col, value)

                # tell the grid we've added a row
                msg = wx.grid.GridTableMessage(self,  # The table
                                               wx.grid.GRIDTABLE_NOTIFY_ROWS_APPENDED,  # what we did to it
                                               1  # how many
                                               )

                self.GetView().ProcessTableMessage(msg)

        innerSetValue(row, col, value)

        # --------------------------------------------------

    # Some optional methods
    # Called when the grid needs to display labels
    def GetColLabelValue(self, col):
        return self.colLabels[col]


class MyFileDropTarget(wx.FileDropTarget):
    def __init__(self, window):
        wx.FileDropTarget.__init__(self)
        self.window = window

    def OnDropFiles(self, x, y, filenames):
        #         print filenames
        for file in filenames:
            self.window.openWisfile(file)


if __name__ == '__main__':
    app = myapp(sys.argv)
    app.statub.SetStatusText("")
    app.MainLoop()
