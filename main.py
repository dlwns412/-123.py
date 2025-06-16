import pandas as pd

# 원본 데이터 예: year_gender_age

# 1) 긴 형태로 변환
df_long = year_gender_age.melt(
    id_vars=["법정전염병군별(1)", "법정전염병군별(2)"], 
    var_name="기간", 
    value_name="발생수"
)

# 2) 발생수 숫자형 변환 (필요하면)
df_long["발생수"] = pd.to_numeric(df_long["발생수"], errors='coerce').fillna(0)

# 3) 성병 관련 감염병 키워드 목록 (예시)
sti_keywords = ["임질", "매독", "클라미디아", "헤르페스", "HIV", "에이즈", "성병"]

# 4) 필터링
df_sti = df_long[df_long["법정전염병군별(1)"].str.contains('|'.join(sti_keywords), na=False)]

# df_sti를 이용해 그래프 그리기 가능
