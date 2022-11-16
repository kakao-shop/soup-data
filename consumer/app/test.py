def beforeTime(time):
    data  = time.split("-")
    minute = int(data[-1])
    hour = int(data[-2]) 
    remain = minute - 30
    if remain >= 0:
        data[-2], data[-1] = str(hour), str(remain)
    else:
        if hour == 0:
            data[-2], data[-1] = str(23), str(60+remain)
        else:
            data[-2], data[-1] =  str(hour-1), str(60+remain)
    if data[-1] == "0":
        data[-1]="00"
    if len(data[-2]) == 1:
        data[-2]= "0" + data[-2]   
    return "-".join(data)

date = "product-2022-11-17-00-30"
print(beforeTime(date))