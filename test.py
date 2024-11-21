import sqlite3


conn = sqlite3.connect("202312.db")
table_name = "teacher_info"
c = conn.cursor()

file = "source/政府雇员名单.txt"
list = []
with open(file, 'r') as file:
    for line in file:
        list.append(line.strip())

#print(list.__len__())

result_list = []
none_list = []
result = []
count = 0
for name in list:
    result = []
    try:
        c.execute("select * from " + table_name + " where name == '" + name + "'")
        result = c.fetchall()
        #print(result)

        if(result != []):
            result_list.append(result)
        else:
            none_list.append(name)

    except Exception as e:
        ##print("执行mysql语句时报错：%s" % e)
        count = count + 1

    finally:
        conn.commit()

print(result_list)
print(none_list.__len__())


# from openpyxl import *
# wb = Workbook()
#
# # 取得当前活动worksheet对象
# ws = wb.active
#
# for row in result_list:
#     for col in row:
#         ws.append(col)
#
# wb.save(".\output\查到的名单.xlsx")





