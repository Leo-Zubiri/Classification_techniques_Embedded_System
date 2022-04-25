a = ['102', '123', '1214', '1244', '323', '744', '539', '2']
a = '102, 123, 1214, 1244, 323, 744, 539, 2'
x = 5

a = list(map(int, a.split(",")))[:x]
vStr = str(a)
l = len(vStr)

vStr = vStr[1:l-1]

print(vStr)

