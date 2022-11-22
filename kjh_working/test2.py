import schedule
import time    
from datetime import datetime
from pytz import timezone
index_name= ""
now = datetime.now(timezone('Asia/Seoul')).minute
print("current minute", now)
if now < 29:
    index_name = "product-"+datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d-%H-')+"00"
else:
    index_name = "product-"+datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d-%H-')+"30"
print(index_name)
# a="0"
# if len(a) ==1:
#     a = "0" + a
# print(a)
# CatAndSubcat = {}
# CatAndSubcat["과일"]=[    "감/홍시","사과","귤","포도","열대과일","견과/밤","키위","배","토마토",
# "자몽","아보카도","바나나","기타만감류","메론","오렌지","레몬/라임","무화과",
# "베리류","파인애플","수박","딸기","기타과일","견과/밤/대추"]

# CatAndSubcat["채소"]=[
#     "마/우엉","무/열무","토마토","버섯","배추/절임배추","샐러드","샐러드채소","감자",
# "호박","나물","옥수수","고추","양파","파프리카","당근","인삼/더덕/약선재료","오이",
# "반찬채소","쌈채소","쪽파","브로콜리","연근","생강","가지","피망",
# "양상추","얼갈이","토란","아스파라거스","기타채소","대파"]

# CatAndSubcat["축산"]=[
# "가공육","돼지고기","소고기","계란/알류","수입육","닭가슴살","닭","한우",
# "기타정육","기타축산","오리고기"]


# CatAndSubcat["수산/건어물"]=[    "건어물","김/파래김","어패류","새우","갑각류","구색선어","오징어",
# "갈치/삼치/고등어","문어","알/해삼","쭈꾸미","연어/참치","가자미","동태/명태",
# "기타수산","낙지"]

# CatAndSubcat["쌀/잡곡"] =[    "쌀","잡곡","현미","흑미","견과","건조식품","건조과일","깨",
# "콩","조","유기농","씨앗"]

# CatAndSubcat["제과/빵"]=[
# "초콜릿","과자","쿠키","시리얼","커피","튀김","빵","간식류소시지","떡","아이스크림"
# ,"캔디","소스"]

# CatAndSubcat["생수/음료"]=[
#     "커피","건강식품","탄산","차","과일/야채음료","생수/탄산수"
# ,"기타음료","코코아/핫초코","전통음료","꿀","이온음료"
# ]

# CatAndSubcat["냉장/냉동식품"]=[
# "김치/젓갈","밀키트","면류","요거트/요구르트","국/탕/찜","만두","반찬/절임류","아이스크림"
# ,"오일/기름","볶음/구이","우유","돈까스/너겟/치킨","과일/야채음료","두부/유부"
# ,"맛집","어묵/유부/크래미","피자/핫도그","베이컨/소시지","냉동과일"
# ,"안주/전류","치즈/버터","볶음밥/덮밥/죽","떡볶이/떡사리","젤리/푸딩"
# ,"감자튀김/치즈스틱","떡갈비/함박스테이크","닭가슴살","두유"
# ,"계란/알류","튀김류","샌드위치/버거","기타식품","베이커리"]

# CatAndSubcat["즉석식품/양념"]=[
# "국/탕/찜","즉석밥","안주/전류","죽/스프","카레/짜장","소금/설탕","스팸/햄"
# ,"도시락","참치캔","꿀","라면","통조림","소스","오일/기름","밀키트","고춧가루/참깨"
# ,"다시다/미원","볶음/구이","사리얼","고추장/된장/간장","닭가슴살","만두","맛술/액젓"
# ,"식초/물엿","돈까스/너겟/치킨","제빵믹스","기타즉석","피자/핫도그","어묵/유부/크래미"
# ,"떡볶이/떡사리","시럽/잼","튀김류","케찹/마요네즈","떡갈비/함박스테이크","건어물"
# ,"베이컨/소시지","드레싱","새우","문어","쭈꾸미"]

# for cat in CatAndSubcat:
#     for subcat in CatAndSubcat[cat]:
#         print(subcat)


# # def beforeTime(time):
# #     data  = time.split("-")
# #     minute = int(data[-1])
# #     hour = int(data[-2]) 

# #     # 분에서 30을 빼고 양수인 경우 그대로
# #     # 음수인 경우 시간에서 1을 빼고
# #     # 초과한 값을 60에서 뺀 값을 분으로 한다.
# #     remain = minute - 30
# #     if remain >= 0:
# #         data[-2], data[-1] = str(hour), str(remain)
# #     else:
# #         # 만약 시간이 0이라면 23시가 돼야 하기 때문에 hour를 23으로 출력다.
# #         if hour == 0:
# #             data[-2], data[-1] = str(23), str(60+remain)
# #         else:
# #             data[-2], data[-1] =  str(hour-1), str(60+remain)
    
# #     return "-".join(data)
# # currentIndex= "product-2022-11-10-21-00"
# # deleteIndexName = beforeTime(currentIndex)
# # print(deleteIndexName)
# # def printhello():
# #     print("Hello!")
 
 
# # schedule.every(1).minutes.do(printhello) #30분마다 실행
 
# # #실제 실행하게 하는 코드
# # while True:
# #     schedule.run_pending()
# #     time.sleep(1)


# # count = [5,2,3]
# # lenCount = len(count)
# # tmp = sum(count)
# # cnt =0
# # result = []
# # while True:
# #     re = 0
# #     result = []
# #     for i in range(lenCount):
# #         re += int((count[i]/tmp)*10)
# #         result.append(int((count[i]/tmp)*10))
# #     if re != 10:
# #         count[cnt%lenCount]=count[cnt%lenCount] +1
# #     else: break
# #     cnt+=1
# # print(result)
# # print(count[0]/(sum(count)))

