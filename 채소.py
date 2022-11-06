# 정답 데이터 만들기  // 채소

# df.loc[df['prdName'].str.contains("사과","과"), "분류"] = "사과"
df.loc[df['prdName'].str.contains("감자"), "분류"] = "감자"
df.loc[df['prdName'].str.contains("고구마"), "분류"] = "고구마"
df.loc[df['prdName'].str.contains("토란"), "분류"] = "토란"
df.loc[df['prdName'].str.contains("마늘"), "분류"] = "마늘"
df.loc[df['prdName'].str.contains("양파"), "분류"] = "양파"
df.loc[df['prdName'].str.contains("대파"), "분류"] = "대파"
df.loc[df['prdName'].str.contains("쪽파"), "분류"] = "쪽파"
df.loc[df['prdName'].str.contains("생강"), "분류"] = "생강"
df.loc[df['prdName'].str.contains("당근"), "분류"] = "당근"
df.loc[df['prdName'].str.contains("연근"), "분류"] = "연근"
df.loc[df['prdName'].str.contains("참마", "장마","산마","야콘","우엉"), "분류"] = "마/우엉"
df.loc[df['prdName'].str.contains("가지"), "분류"] = "가지"
df.loc[df['prdName'].str.contains("오이", "생수세미"), "분류"] = "오이"
df.loc[df['prdName'].str.contains("파프피카", "스위트파피"), "분류"] = "파프리카"
df.loc[df['prdName'].str.contains("브로콜리","콜리"), "분류"] = "브로콜리"
df.loc[df['prdName'].str.contains("피망"), "분류"] = "피망"

df.loc[df['prdName'].str.contains("로메인","카이피라","레터스","비트","파슬리","이자트릭스","프릴아이스","스탠포드","신선초","알로에","바질"), "분류"] = "샐러드채소"
df.loc[df['prdName'].str.contains("샐러리","케일"), "분류"] = "샐러리"
df.loc[df['prdName'].str.contains("아스파라거스"), "분류"] = "아스파라거스"
df.loc[df['prdName'].str.contains("양상"), "분류"] = "양상추"

df.loc[df['prdName'].str.contains("적상추", "청상추","혼합 상추","포기 상추"), "분류"] = "상추"
df.loc[df['prdName'].str.contains("알배기","쌈채소","적겨자","당귀","쌈추","치커리","새싹삼","청경채","향나물","치콘","참나물","레디쉬","근대","고수","쌈케일"), "분류"] = "쌈채소"
df.loc[df['prdName'].str.contains("깻잎"), "석류"] = "깻잎"
df.loc[df['prdName'].str.contains("고추"), "분류"] = "고추"


df.loc[df['prdName'].str.contains("알타리","열무","절단 무","월동무","세척무","무우","무(국산","국내산 무"), "분류"] = "무"
df.loc[df['prdName'].str.contains("배추 (통","봄동","절임배추","배추"), "분류"] = "배추/절임배추"
df.loc[df['prdName'].str.contains("양배", "송이"), "분류"] = "양배추"

df.loc[df['prdName'].str.contains("얼갈이","홍갓","청갓"), "분류"] = "얼갈이"

df.loc[df['prdName'].str.contains("버섯","동충하초","표고","느타리","새송이"), "분류"] = "버섯"
df.loc[df['prdName'].str.contains("시금치","부추","미나리","국거리채소","생나물","쑥갓","달래","세발나물","취나물","깻순","유채","공심채","돌나물","도라지","돌산갓","머위잎","방풍나물","신선초","고구마순"), "분류"] = "반찬채소"
df.loc[df['prdName'].str.contains("미역","다시마","톳","꼬시래기","죽순","시래기","토란대","고사리","궁채나물","곤드레","우거지","취나물"), "분류"] = "나물/해초"
df.loc[df['prdName'].str.contains("샐러드","무순","어린잎","아이순","채소믹스","드레싱","오크라","야채믹스","스피아민트","레드키드니빈","칙피","완두순","페퍼민트","레몬그라스","궁채",""), "분류"] = "샐러드"

df.loc[df['prdName'].str.contains("석류","수삼","즙","산삼","더덕","장뇌삼","흑화고","인삼","수삼","속편해"), "분류"] = "인삼/더덕/약선재료"



df