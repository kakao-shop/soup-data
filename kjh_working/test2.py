
count = [5,2,3]
lenCount = len(count)
tmp = sum(count)
cnt =0
result = []
while True:
    re = 0
    result = []
    for i in range(lenCount):
        re += int((count[i]/tmp)*10)
        result.append(int((count[i]/tmp)*10))
    if re != 10:
        count[cnt%lenCount]=count[cnt%lenCount] +1
    else: break
    cnt+=1
print(result)
print(count[0]/(sum(count)))

