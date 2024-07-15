import math
x,y = input().split(" ")
if int(x) > int(y):
    print("2")
else:
    print(math.ceil(int(y)/int(x)))