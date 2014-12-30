import xlrd
print("ConfigTool>>>>")
book = xlrd.open_workbook("CS.xlsx")
print "The number of worksheets is", book.nsheets
print "Worksheet name(s):", book.sheet_names()
sh = book.sheet_by_index(0)
print sh.name, sh.nrows, sh.ncols
print "Cell A11 is", sh.cell_value(rowx=0, colx=0)
for rx in range(sh.nrows):
    print sh.row(rx)
# Refer to docs for more details.
# Feedback on API is welcomed.