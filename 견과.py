# 정답 데이터 만들기  // 견과

# df.loc[df['prdName'].str.contains("사과","과"), "분류"] = "사과"
df.loc[df['prdName'].str.contains("누룽지","오트밀","넛츠","잣","미숫가루","귀리","분말","프로틴","곡물","가루","곤약","곡식","엄마애손","산과들에","시드","호박씨","아몬드","건호두","견과","땅콩","알토란칩","크런치","해바라기씨","호두","땅콩","몬드",""), "분류"] = "견과/건강분말"



df