# 정답 데이터 만들기  // 수산

# df.loc[df['prdName'].str.contains("사과","과"), "분류"] = "사과"
df.loc[df['prdName'].str.contains("가자미","홍어","가오리"), "분류"] = "가자미"
df.loc[df['prdName'].str.contains("갈치","삼치","고등어","박대"), "분류"] = "갈치/삼치/고등어"
df.loc[df['prdName'].str.contains("민물장어","꽁치","아귀","전어","도미","우럭","병어","민어","양미리","옥돔","복어","과매기","대구","어란","임연수","꽃돔","감성돔","선어","병어"), "분류"] = "구색선어"
df.loc[df['prdName'].str.contains("동태","명태","코다리"), "분류"] = "동태"
df.loc[df['prdName'].str.contains("연어"), "분류"] = "연어"

df.loc[df['prdName'].str.contains("크랩","랍스터","대게","꽃게","홍게"), "분류"] = "크랩류"
df.loc[df['prdName'].str.contains("새우"), "분류"] = "새우"

df.loc[df['prdName'].str.contains("오징어"), "분류"] = "오징어"
df.loc[df['prdName'].str.contains("낙지"), "분류"] = "낙지"
df.loc[df['prdName'].str.contains("쭈꾸미"), "분류"] = "쭈꾸미"
df.loc[df['prdName'].str.contains("문어"), "분류"] = "문어"

df.loc[df['prdName'].str.contains("홍합","바지락","관자","전복","가리비","꼬막","조개","우렁","소라","굴","대합","거북손","동죽"), "분류"] = "어패류"


df.loc[df['prdName'].str.contains("우육포","진미채","멸치","쥐포","황태","아귀포","숏다리","진짜바삭한","코주부","오족","명엽채","양태","건보리새우","왕다리","홍진미","백진미","왕대발","뱅어포","육포","마른안주","먹태","한치","수염새우","땅콩버터","장족","꾸이"), "분류"] = "건어물"


df.loc[df['prdName'].str.contains("김","미역","매생이","파래","해초","다시마",""), "분류"] = "해조류"



df