import random
a=random.randint(1,100)
print("随机一个1-100之间的数字，开始吧！")
for i in range(0,5):
    print("第",i,"次猜数字：")
    b=input()
    b=int(b)
    if b<a:
        print("猜小了")
    elif b>a:
        print("猜大了")
    else:
        print("猜对了")
        break
print("游戏结束xixixixii")
