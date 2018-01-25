import xlwt



list1=[2.34,4.346,4.234]

book = xlwt.Workbook(encoding="utf-8")

sheet1 = book.add_sheet("Sheet 1")

sheet1.write(0, 0, "Rank")
sheet1.write(0, 1, "Title")
sheet1.write(0, 2, "Artist")
sheet1.write(0, 3, "Album")



i=4

for n in list1:
    i = i+1
    sheet1.write(i, 0, n)



book.save("trial.xls")