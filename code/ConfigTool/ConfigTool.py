#coding: utf-8
import xlrd
import xlwt

print("ConfigTool>>>>")
book = xlrd.open_workbook("CS.xlsx")
sh = book.sheet_by_index(0)


serverBook = xlwt.Workbook(encoding='utf-8', style_compression=0)  
serverSheet = serverBook.add_sheet('sheet', cell_overwrite_ok=True) 
serverCol = 0

clientBook = xlwt.Workbook(encoding='utf-8', style_compression=0)
clientSheet = clientBook.add_sheet('sheet', cell_overwrite_ok=True)
clientCol = 0

for cx in range(sh.ncols):
	cel = sh.col(cx)
	# print(cel)
	typeFlag = cel[0].value
	# print typeFlag
	if typeFlag == "CS" or typeFlag == "S":	
		for vx in xrange(1, len(cel)):
			v = cel[vx]
			print vx
			print v
			serverSheet.write(vx - 1, serverCol, v.value)
		serverCol += 1

	if typeFlag == "CS" or typeFlag == "C":
		for vc in xrange(1,len(cel)):
			c = cel[vc]
			clientSheet.write(vc - 1, clientCol, c.value)
		clientCol += 1	

serverBook.save("Server.csv")	
clientBook.save("Client.csv")
