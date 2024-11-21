file = open("./新建文本文档.txt","r")

result = file.readlines()
data = []

for i in result:
    data.append(int(i.split()[0]))

print(data)
print(max(data))

label = ["0-5年","6-10年","11-15年","16-20年","21-25年","26-30年","31-35年","36-40年","41-45年","46-50年"]
data1 = []
for i in range(0,len(label)):
    data1.append(0)

for i in data:
    if(i>=0 and i <= 5):
        data1[0] = data1[0] + 1
    elif(i>=6 and i <= 10):
        data1[1] = data1[1] + 1
    elif (i >= 11 and i <= 15):
        data1[2] = data1[2] + 1
    elif (i >= 16 and i <= 20):
        data1[3] = data1[3] + 1
    elif (i >= 21 and i <= 25):
        data1[4] = data1[4] + 1
    elif (i >= 26 and i <= 30):
        data1[5] = data1[5] + 1
    elif (i >= 31 and i <= 35):
        data1[6] = data1[6] + 1
    elif (i >= 36 and i <= 40):
        data1[7] = data1[7] + 1
    elif (i >= 41 and i <= 45):
        data1[8] = data1[8] + 1
    elif (i >= 46):
        data1[9] = data1[9] + 1

print(label)
print(data1)

