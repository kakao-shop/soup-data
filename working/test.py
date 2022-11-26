import time
start = time.time()  # 시작 시간 저장
 
 
# 작업 코드

while(True):
    if time.time() - start > 2: exit()

print("time :", time.time() - start)  # 현재시각 - 시작시간 = 실행 시간


