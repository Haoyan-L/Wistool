# # encoding=gb18030
# import xlrd
# import xlwt
# import re
#
# wildcard = "csv 文件 (*.csv)|*.csv|" \
#            "All files (*.*)|*.*"
#
# import types
#
#
# class pxls:
#     def __init__(self, xlsfile=''):
#         self.xlsf = xlsfile
#         self.bk = None
#         if xlsfile != '':
#             self.bk = self.opbook(self.xlsf)
#
#     def setxls(self, f):
#         self.xlsf = f
#         # print self.xlsf
#         self.bk = self.opbook(self.xlsf)
#
#     def opbook(self, f):
#         return xlrd.open_workbook(self.xlsf, encoding_override='utf-8')
#
#     def get_sheetname(self):
#         return self.bk.sheet_names()
#
#     def get_rowcols(self, shtname):
#         sh = self.bk.sheet_by_name(shtname)
#         return sh.nrows, sh.ncols
#
#     def get_dataoncol1(self, ind, col):
#         sh = self.bk.sheet_by_index(ind)
#         dac = []
#         for mm in sh.col_values(col):
#             if type(mm) == str:
#                 dac.append(mm.encode('gbk'))
#             # print mm.encode('gbk')
#         return dac
#
#     def get_dataoncol(self, shtname, col):
#         sh = self.bk.sheet_by_name(shtname)
#         dac = []
#         for mm in sh.col_values(col):
#             if type(mm) == str:
#                 dac.append(mm.encode('gbk'))
#             # print mm.encode('gbk')
#         return dac
#
#     def get_dataonrow(self, shtname, row):
#
#         sh = self.bk.sheet_by_name(shtname)
#
#         dar = []
#         for dd in sh.row_values(row):
#             if type(dd) == str:
#                 dd = dd.encode('gbk')
#             dar.append(dd)
#             # print dd.encode('gbk')
#         return dar
#         # print sh.cell_value(1,1)
#         # for rx in range(sh.nrows):
#         # print sh.row(rx)
#         # print sh.row_values(rx)
#
#     @staticmethod
#     def savedata(fn, shts=dict()):
#         file = xlwt.Workbook()
#         if len(shts.keys()) > 0:
#             for sht in shts.keys():
#                 table = file.add_sheet(sht, cell_overwrite_ok=True)
#                 datas = shts[sht]
#                 for x in range(len(datas)):
#                     for y in range(len(datas[0])):
#                         if type(datas[x][y]) == bytes:
#                             #                             print x,y,datas[x][y]
#                             tm = datas[x][y]
#                             try:
#                                 tm = tm.decode('gbk')
#                             except UnicodeDecodeError as ee:
#                                 print(tm + "con't decode string!")
#                                 continue
#                             table.write(x, y, tm)
#                         else:
#                             table.write(x, y, datas[x][y])
#         file.save(fn)
#
#
# #         print len(fn)
#
# class str_anal:
#
#     ##gbk编码搜素，同文件头设置的默认编码#encoding=gb18030
#     @staticmethod
#     def search_jh(st):
#         szPattern = "(^[\x8140-\xFEFE]{1,6}\d+\-{0,1}\w*).*"
#         xx = re.match(szPattern, st)
#         if xx != None:
#             return xx.group(1)
#         else:
#             return 'jh not found'
#
#     # unicode 编码搜素
#     @staticmethod
#     def search_jhu(st):
#         #         st=unicode(st)
#         szPattern = u"(^[\u4e00-\u9fa5\u0041-\u005a]{1,3}\d+\-{0,1}\w*).*"
#         xx = re.match(szPattern, st)
#         if xx != None:
#             return xx.group(1).encode('gb18030')
#         else:
#             return 'jh not found'